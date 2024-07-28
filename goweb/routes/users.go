package routes

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func addUserRoutes(rg *gin.RouterGroup) {
	users := rg.Group("/users")

	users.GET("/", func(c *gin.Context) {
		c.JSON(http.StatusOK, "users")
	})

	users.GET("/comments", func(c *gin.Context) {
		c.JSON(http.StatusOK, "users comments")
	})

	users.GET("/pictures", func(c *gin.Context) {
		c.JSON(http.StatusOK, "users pictures")
	})

	users.GET("/search/:username/:address", func(c *gin.Context) {
		username := c.Param("username")
		address := c.Param("address")
		c.JSON(http.StatusOK, gin.H{
			"message":  "ok",
			"username": username,
			"address":  address,
		})
	})
}
