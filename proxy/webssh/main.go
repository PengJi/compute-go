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

		// Gets a list of errors for the specified type
		detectedErrors := c.Errors.ByType(errType)
		if len(detectedErrors) > 0 {
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

			c.IndentedJSON(parsedError.Code, parsedError)
			return
		}
	}
}

func CORSMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
		c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
		c.Writer.Header().Set("Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
		c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

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
