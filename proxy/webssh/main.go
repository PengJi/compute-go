package main

import (
	"net/http"
	"os"

	"github.com/gin-gonic/gin"

	"webssh/views"
)

var (
	EnvGOPATH     = os.Getenv("GOPATH")
	TemplateFiles = "/home/jipeng/compute-go/proxy/webssh/templates/*.html"
	StaticFiles   = "/home/jipeng/compute-go/proxy/webssh/templates/static"
)

// handle any errors encountered
func JSONAppErrorReporter() gin.HandlerFunc {
	return jsonAppErrorReporterT(gin.ErrorTypeAny)
}

func jsonAppErrorReporterT(errType gin.ErrorType) gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Next()

		// 获取指定类型的错误列表
		detectedErrors := c.Errors.ByType(errType)
		if len(detectedErrors) > 0 {
			// 取第一个错误进行处理
			err := detectedErrors[0].Err

			var parsedError *views.ApiError

			switch e := err.(type) {
			case *views.ApiError:
				parsedError = e
			default:
				parsedError = &views.ApiError{
					Code:    http.StatusInternalServerError,
					Message: err.Error(),
				}
			}

			// 返回格式化的 JSON 响应
			c.IndentedJSON(parsedError.Code, parsedError)
			return
		}
	}
}

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		// 设置允许所有域访问资源的响应头
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		// 设置是否允许发送Cookie信息（允许跨域请求发送凭证）
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		// 设置允许的请求头
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		// 设置允许的HTTP请求方法
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")

		// 如果是OPTIONS请求，则直接返回204状态码并终止请求链
		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		// 继续处理接下来的中间件或请求
		c.Next()
	}
}

func main() {
	server := gin.Default()
	server.LoadHTMLGlob(TemplateFiles)
	server.Static("/static", StaticFiles)

	server.Use(JSONAppErrorReporter())
	server.Use(CORSMiddleware())

	server.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})
	server.GET("/ws", views.ShellWs)

	server.Run("0.0.0.0:5001")
}
