package main

import (
	"archive/zip"
	"fmt"
	"io"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/gin-gonic/gin"
)

func main() {
	// 创建一个 Gin 路由器
	r := gin.Default()

	// 文件上传路由
	r.POST("/efile/openapi/v2/file/upload", uploadFileHandler)

	// 文件/文件夹下载路由
	r.GET("/efile/openapi/v2/file/download", downloadFileHandler)

	// 启动 Web 服务，监听 8080 端口
	r.Run("0.0.0.0:8080")
}

// uploadFileHandler 处理文件上传请求
func uploadFileHandler(c *gin.Context) {
	// 验证 token
	if !validateToken(c) {
		return
	}

	// 获取和验证路径参数
	path, cover, file, err := parseUploadParams(c)
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"code": "1", "data": nil, "msg": err.Error()})
		return
	}

	// 保存文件
	err = saveUploadedFile(c, file, path, cover)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"code": "1", "data": nil, "msg": err.Error()})
		return
	}

	// 返回成功响应
	c.JSON(http.StatusOK, gin.H{"code": "0", "data": nil, "msg": "success"})
}

// downloadFileHandler 处理文件/文件夹下载请求
func downloadFileHandler(c *gin.Context) {
	// 验证 token
	if !validateToken(c) {
		return
	}

	// 获取路径参数
	path := c.Query("path")
	if path == "" {
		c.JSON(http.StatusBadRequest, gin.H{"code": "1", "data": nil, "msg": "path is required"})
		return
	}

	// 判断是文件还是文件夹
	info, err := os.Stat(path)
	if os.IsNotExist(err) {
		c.JSON(http.StatusNotFound, gin.H{"code": "1", "data": nil, "msg": "file or directory not found"})
		return
	}

	if info.IsDir() {
		// 压缩并下载文件夹
		downloadDirectory(c, path)
	} else {
		// 处理文件下载，支持断点续传
		downloadFile(c, path, info)
	}
}

// validateToken 验证请求头中的 token
func validateToken(c *gin.Context) bool {
	token := c.GetHeader("token")
	if token == "" {
		c.JSON(http.StatusBadRequest, gin.H{"code": "1", "data": nil, "msg": "token is required"})
		return false
	}
	return true
}

// parseUploadParams 解析并验证上传请求的参数
func parseUploadParams(c *gin.Context) (string, string, *multipart.FileHeader, error) {
	path := c.PostForm("path")
	if path == "" {
		return "", "", nil, fmt.Errorf("path is required")
	}

	cover := c.DefaultPostForm("cover", "uncover")
	file, err := c.FormFile("file")
	if err != nil {
		return "", "", nil, fmt.Errorf("file is required")
	}

	return path, cover, file, nil
}

// saveUploadedFile 保存上传的文件
func saveUploadedFile(c *gin.Context, file *multipart.FileHeader, path, cover string) error {
	savePath := filepath.Join(path, file.Filename)

	// 检查是否需要覆盖文件
	if cover == "uncover" {
		if _, err := os.Stat(savePath); err == nil {
			return fmt.Errorf("file already exists")
		}
	}

	// 保存文件
	return c.SaveUploadedFile(file, savePath)
}

// downloadDirectory 压缩并下载文件夹
func downloadDirectory(c *gin.Context, path string) {
	zipPath := filepath.Base(path) + ".zip"
	err := zipDirectory(path, zipPath)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"code": "1", "data": nil, "msg": "failed to zip directory"})
		return
	}
	defer os.Remove(zipPath) // 下载后删除压缩文件

	c.Header("Content-Type", "application/zip")
	c.Header("Content-Disposition", fmt.Sprintf("attachment; filename=%s", zipPath))
	c.File(zipPath)
}

// downloadFile 处理文件下载，支持断点续传
func downloadFile(c *gin.Context, path string, info os.FileInfo) {
	c.Header("Content-Type", "application/octet-stream")
	c.Header("Content-Disposition", fmt.Sprintf("attachment; filename=%s", filepath.Base(path)))

	// 处理断点续传
	rangeHeader := c.GetHeader("Range")
	if rangeHeader != "" {
		c.Header("Accept-Ranges", "bytes")
		file, err := os.Open(path)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"code": "1", "data": nil, "msg": "failed to open file"})
			return
		}
		defer file.Close()

		// 解析 Range 头
		var start, end int64
		if _, err := fmt.Sscanf(rangeHeader, "bytes=%d-%d", &start, &end); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"code": "1", "data": nil, "msg": "invalid Range header"})
			return
		}
		fileSize := info.Size()
		if end == 0 || end >= fileSize {
			end = fileSize - 1
		}

		// 设置响应头
		c.Header("Content-Range", fmt.Sprintf("bytes %d-%d/%d", start, end, fileSize))
		c.Status(http.StatusPartialContent)

		// 发送文件部分内容
		_, err = file.Seek(start, 0)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"code": "1", "data": nil, "msg": "failed to seek file"})
			return
		}
		io.CopyN(c.Writer, file, end-start+1)
	} else {
		// 正常下载文件
		c.File(path)
	}
}

// zipDirectory 压缩文件夹为 zip 文件
func zipDirectory(source, target string) error {
	zipFile, err := os.Create(target)
	if err != nil {
		return err
	}
	defer zipFile.Close()

	zipWriter := zip.NewWriter(zipFile)
	defer zipWriter.Close()

	return filepath.Walk(source, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		// 创建压缩文件头
		header, err := zip.FileInfoHeader(info)
		if err != nil {
			return err
		}

		header.Name = strings.TrimPrefix(path, filepath.Dir(source)+"/")
		if info.IsDir() {
			header.Name += "/"
		} else {
			header.Method = zip.Deflate
		}

		writer, err := zipWriter.CreateHeader(header)
		if err != nil {
			return err
		}

		// 如果不是目录，写入文件内容
		if !info.IsDir() {
			file, err := os.Open(path)
			if err != nil {
				return err
			}
			defer file.Close()
			_, err = io.Copy(writer, file)
			if err != nil {
				return err
			}
		}
		return nil
	})
}
