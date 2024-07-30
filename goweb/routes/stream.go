package routes

import (
	"fmt"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

func testSteamGET(ctx *gin.Context) {
	w := ctx.Writer
	header := w.Header()
	header.Set("Transfer-Encoding", "chunked")
	header.Set("Content-Type", "text/html")
	w.WriteHeader(http.StatusOK)

	w.Write([]byte(`test streaming`))
	w.(http.Flusher).Flush()

	w.Write([]byte(`
		<html>
				<body>
	`))
	w.(http.Flusher).Flush()

	for i := 0; i < 10; i++ {
		w.Write([]byte(fmt.Sprintf(`
			<h1>%d</h1>
		`, i)))
		w.(http.Flusher).Flush()
		time.Sleep(time.Duration(1) * time.Second)
	}

	w.Write([]byte(`
		
				</body>
		</html>
	`))
	w.(http.Flusher).Flush()
}

func AddStreamRoutes(router *gin.Engine) {
	router.GET("/test_stream", testSteamGET)
}

/*
browser test url:
http://127.0.0.1:8080/test_stream
*/
