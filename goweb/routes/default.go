package routes

import (
	"net/http"

	"goweb/middleware"

	"github.com/gin-gonic/gin"
)

func AddDefaultRoutes(router *gin.Engine) {
	// register middle ware StatCost
	router.GET("/", middleware.StatCost(), func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Hello world!",
		})
	})
}
