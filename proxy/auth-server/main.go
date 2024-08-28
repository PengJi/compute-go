package main

import (
	"net/http"
	"time"

	"github.com/dgrijalva/jwt-go"
	"github.com/gin-gonic/gin"
)

// 区域信息结构体
type ClusterInfo struct {
	ClusterName string `json:"clusterName"`
	ClusterId   string `json:"clusterId"`
	Token       string `json:"token"`
}

// 响应消息结构体
type Response struct {
	Msg  string        `json:"msg"`
	Code string        `json:"code"`
	Data []ClusterInfo `json:"data"`
}

// 用户认证结构体
type AuthRequest struct {
	User     string `header:"user" binding:"required"`
	Password string `header:"password" binding:"required"`
	OrgId    string `header:"orgId" binding:"required"`
}

// Token验证响应结构体
type TokenValidationResponse struct {
	Msg  string `json:"msg"`
	Code string `json:"code"`
	Data string `json:"data"`
}

// JWT 密钥
var jwtKey = []byte("secret_key")

// 模拟获取区域信息
func getClusterInfo(user string) []ClusterInfo {
	clusters := []ClusterInfo{
		{"OpenAPI计算中心", "11112", ""},
		{"test中心", "111131", ""},
		{"ac", "0", ""},
	}

	for i, cluster := range clusters {
		// 模拟账户状态为 "active" 或 "disabled"
		accountStatus := "active"
		if cluster.ClusterName == "test中心" {
			accountStatus = "disabled"
		}

		if accountStatus == "active" || cluster.ClusterId == "0" {
			token := generateToken(user, cluster.ClusterId, accountStatus)
			clusters[i].Token = token
		} else {
			// 停用状态不生成token，保持为null
			clusters[i].Token = ""
		}
	}

	return clusters
}

// 生成JWT Token
func generateToken(user string, clusterId string, accountStatus string) string {
	claims := jwt.MapClaims{
		"username":      user,
		"clusterId":     clusterId,
		"accountStatus": accountStatus,
		"exp":           time.Now().Add(time.Hour * 1).Unix(),
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, _ := token.SignedString(jwtKey)
	return tokenString
}

// 认证授权处理函数
func authHandler(c *gin.Context) {
	var authRequest AuthRequest

	if err := c.ShouldBindHeader(&authRequest); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"msg": "Invalid headers", "code": "1"})
		return
	}

	// 模拟认证逻辑
	if authRequest.User == "test" && authRequest.Password == "111111" {
		clusters := getClusterInfo(authRequest.User)
		c.JSON(http.StatusOK, Response{
			Msg:  "success",
			Code: "0",
			Data: clusters,
		})
	} else {
		c.JSON(http.StatusUnauthorized, gin.H{"msg": "Unauthorized", "code": "401"})
	}
}

// 验证Token合法性
func validateToken(tokenString string) bool {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		return jwtKey, nil
	})

	if err != nil {
		return false
	}

	if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
		// 可以在此处进一步检查Claims中的数据，如过期时间
		_ = claims["username"] // 示例获取username
		return true
	}

	return false
}

// Token验证处理函数
func tokenValidationHandler(c *gin.Context) {
	tokenString := c.GetHeader("token")

	if tokenString == "" {
		c.JSON(http.StatusBadRequest, TokenValidationResponse{
			Msg:  "missing token",
			Code: "1",
			Data: "token is missing",
		})
		return
	}

	if validateToken(tokenString) {
		c.JSON(http.StatusOK, TokenValidationResponse{
			Msg:  "success",
			Code: "0",
			Data: "token is valid",
		})
	} else {
		c.JSON(http.StatusUnauthorized, TokenValidationResponse{
			Msg:  "failure",
			Code: "401",
			Data: "token is invalid",
		})
	}
}

func main() {
	r := gin.Default()
	r.POST("/ac/openapi/v2/tokens", authHandler)
	r.GET("/ac/openapi/v2/tokens/state", tokenValidationHandler)
	r.Run("0.0.0.0:8080")
}
