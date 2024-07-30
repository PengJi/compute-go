package main

import (
	"context"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"syscall"
	"time"

	"goweb/config"
	"goweb/db"
	"goweb/logger"
	"goweb/routes"
)

var ()

func main() {
	log := logger.GetLogger()
	log.Info("application starting")

	log.Info("loading configuration")
	config.LoadConfig()

	log.Info("initing mysql database")
	db.InitDB()

	log.Info("setting routes")
	router := routes.SetRoutes()

	// Create context that listens for the interrupt signal from the OS.
	ctx, stop := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer stop()

	srv := &http.Server{
		Addr:    ":" + strconv.Itoa(config.AppConfig.Server.Port),
		Handler: router,
	}

	// Initializing the server in a goroutine so that
	// it won't block the graceful shutdown handling below
	// log.Info("Starting server", config.AppConfig.Server.Port)
	log.Info("Starting server", "port", config.AppConfig.Server.Port)
	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Error("listen:", slog.Any("err", err))
		}
	}()

	// Listen for the interrupt signal.
	<-ctx.Done()

	// Restore default behavior on the interrupt signal and notify user of shutdown.
	stop()
	log.Info("shutting down gracefully, press Ctrl+C again to force")

	// The context is used to inform the server it has 5 seconds to finish
	// the request it is currently handling
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	if err := srv.Shutdown(ctx); err != nil {
		log.Error("Server forced to shutdown: ", slog.Any("err", err))
		os.Exit(1)
	}

	log.Info("Server exited")
}
