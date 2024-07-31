package routes

import (
	"bufio"
	"bytes"
	"encoding/json"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

// llama response data
type StreamData struct {
	Model     string    `json:"model"`
	CreatedAt time.Time `json:"created_at"`
	Response  string    `json:"response"`
	Done      bool      `json:"done"`
}

var (
	ollamaURL = "http://192.168.124.25:11434/api/generate"
	llmModel  = "llama3.1"
)

func reqEcho(ctx *gin.Context) {
	w, r := ctx.Writer, ctx.Request
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Error("websocket, upgrade", "err", err)
		return
	}
	defer c.Close()

	for {
		mt, message, err := c.ReadMessage()
		if err != nil {
			log.Error("read message", "err", err)
			break
		}
		log.Info("recv", "message", message)

		reqMessage := string(message)
		requestBody, err := json.Marshal(map[string]string{
			"model":  llmModel,
			"prompt": reqMessage,
		})
		if err != nil {
			log.Error("Error creating request body", "err", err)
			return
		}

		req, err := http.NewRequest("POST", ollamaURL, bytes.NewBuffer(requestBody))
		if err != nil {
			log.Error("Error creating request", "err", err)
			return
		}
		req.Header.Set("Content-Type", "application/json")

		resp, err := http.DefaultClient.Do(req)
		if err != nil {
			log.Error("Error making request", "err", err)
			return
		}
		defer resp.Body.Close()
		if resp.StatusCode != http.StatusOK {
			log.Error("Unexpected status code", "err", resp.StatusCode)
		}

		var respStr bytes.Buffer
		var data StreamData
		scanner := bufio.NewScanner(resp.Body)
		for scanner.Scan() {
			// scan each line
			line := scanner.Text()
			if err := scanner.Err(); err != nil {
				log.Error("Error reading stream", "err", err)
				break
			}

			err := json.Unmarshal([]byte(line), &data)
			if err != nil {
				log.Error("Error parsing JSON", "err", err)
				continue
			}

			// fmt.Printf("Received data: Model=%s, CreatedAt=%s, Response=%s, Done=%v\n", data.Model, data.CreatedAt, data.Response, data.Done)
			// check if is last line
			if data.Done {
				break
			}

			respStr.WriteString(data.Response)
		}

		err = c.WriteMessage(mt, respStr.Bytes())
		if err != nil {
			log.Error("write", "err", err)
			break
		}
	}
}

func req(c *gin.Context) {
	homeTemplate.Execute(c.Writer, "ws://"+c.Request.Host+"/v3/ollama/echo")
}

func AddOllamaRoutes(rg *gin.RouterGroup) {
	web := rg.Group("/ollama")
	web.GET("/", req)
	web.GET("/echo", reqEcho)
}

// API
// /v3/ollama/
