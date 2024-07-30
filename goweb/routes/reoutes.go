package routes

import (
	"github.com/gin-gonic/gin"
	"go.uber.org/ratelimit"

	"goweb/config"
	"goweb/logger"
	"goweb/middleware"
)

var (
	router = gin.Default()
	log    = logger.GetLogger()
	limit  ratelimit.Limiter
)

// getRoutes will create our routes of our entire application
// this way every group of routes can be defined in their own file
// so this one won't be so messy
func SetRoutes() *gin.Engine {
	AddDefaultRoutes(router)
	AddStreamRoutes(router)
	AddCustomerRoutes(router)

	v1 := router.Group("/v1")
	AddUserRoutes(v1)

	v2 := router.Group("/v2")
	AddPingRoutes(v2)

	v3 := router.Group("/v3")
	AddWebSocketRoutes(v3)
	AddOllamaRoutes(v3)

	// router.Use(middleware.StatCost())
	log.Info("registering middle ware")
	limit = ratelimit.New(config.AppConfig.Apilimit.Limit)
	router.Use(middleware.LeakBucket(limit))

	return router
}
