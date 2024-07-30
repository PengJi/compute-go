package routes

import (
	"net/http"

	"github.com/gin-gonic/gin"

	"goweb/db"
	"goweb/middleware"
)

func customerSearchGET(c *gin.Context) {
	name := c.Param("name")
	customer, err := db.GetCustomer(name)
	if err != nil {
		c.JSON(http.StatusFound, gin.H{"error": err.Error()})
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"message": "ok",
		"name":    customer.C_NAME,
		"address": customer.C_ADDRESS,
	})
}

func AddCustomerRoutes(router *gin.Engine) {
	router.GET("/search/:name", middleware.StatCost(), customerSearchGET)
}
