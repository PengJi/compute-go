package routes

import (
	"text/template"

	"github.com/gin-gonic/gin"
	"github.com/gorilla/websocket"

	"goweb/logger"
)

var (
	upgrader = websocket.Upgrader{} // use default option
)

var homeTemplate = template.Must(template.New("").Parse(`
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script>  
window.addEventListener("load", function(evt) {
    var output = document.getElementById("output");
    var input = document.getElementById("input");
    var ws;

    var print = function(message) {
        output.innerHTML += message;
        output.scroll(0, output.scrollHeight);
    };

    document.getElementById("open").onclick = function(evt) {
        if (ws) {
            return false;
        }
        ws = new WebSocket("{{.}}");
        ws.onopen = function(evt) {
            print("OPEN<br>");
        }
        ws.onclose = function(evt) {
            print("<br>CLOSE<br>");
            ws = null;
        }
        ws.onmessage = function(evt) {
            print(evt.data + " "); // response
        }
        ws.onerror = function(evt) {
            print("ERROR: " + evt.data + "<br>");
        }
        return false;
    };

    document.getElementById("send").onclick = function(evt) {
        if (!ws) {
            return false;
        }
        print("<br>" + "SEND: " + input.value + "<br>");
        ws.send(input.value);
        return false;
    };

    document.getElementById("close").onclick = function(evt) {
        if (!ws) {
            return false;
        }
        ws.close();
        return false;
    };
});
</script>
</head>
<body>
<table>
<tr><td valign="top" width="20%">
<p>Click "Open" to create a connection to the server. </p>
<p>Click "Send" to send a message to the server. </p>
<p>Click "Close" to close the connection. </p>
<p>You can change the message and send multiple times.</p>
<form>
<button id="open">Open</button>
<button id="close">Close</button>
<p><input id="input" type="text" value="Hello world!">
<button id="send">Send</button>
</form>
</td><td valign="top" width="50%">
<div id="output" style="max-height: 70vh;overflow-y: scroll;"></div>
</td></tr></table>
</body>
</html>
`))

func echo(ctx *gin.Context) {
	w, r := ctx.Writer, ctx.Request
	c, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		logger.Log.Error("websocket, upgrade", "err", err)
		return
	}
	defer c.Close()

	for {
		mt, message, err := c.ReadMessage()
		if err != nil {
			logger.Log.Error("read message", "err", err)
			break
		}
		logger.Log.Info("recv", "message", message)

		err = c.WriteMessage(mt, message)
		if err != nil {
			logger.Log.Error("write", "err", err)
			break
		}
	}
}

func home(c *gin.Context) {
	homeTemplate.Execute(c.Writer, "ws://"+c.Request.Host+"/v3/websocket/echo")
}

func AddWebSocketRoutes(rg *gin.RouterGroup) {
	web := rg.Group("/websocket")
	web.GET("/", home)
	web.GET("/echo", echo)
}

// API
// /v3/websocket/
// /v3/websocket/echo
