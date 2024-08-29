package views

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"

	"webssh/connection"
)

func ShellWs(c *gin.Context) {
	var upgrader = websocket.Upgrader{
		ReadBufferSize:  2048,
		WriteBufferSize: 2048,
		// TODO
		CheckOrigin: func(r *http.Request) bool {
			return true
		},
	}
	var err error
	msg := c.DefaultQuery("msg", "")
	cols := c.DefaultQuery("cols", "150")
	rows := c.DefaultQuery("rows", "35")
	col, _ := strconv.Atoi(cols)
	row, _ := strconv.Atoi(rows)
	terminal := connection.Terminal{
		Columns: uint32(col),
		Rows:    uint32(row),
	}

	sshClient, err := connection.DecodedMsgToSSHClient(msg)
	if err != nil {
		c.Error(err)
		return
	}
	if sshClient.IpAddress == "" || sshClient.Password == "" {
		c.Error(&ApiError{Message: "IP address/username/password can not be empty", Code: 400})
		return
	}

	conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
	if err != nil {
		c.Error(err)
		return
	}

	err = sshClient.GenerateClient()
	if err != nil {
		conn.WriteMessage(1, []byte(err.Error()))
		conn.Close()
		return
	}

	sshClient.RequestTerminal(terminal)
	sshClient.Run(conn)
}
