package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
)

type RequestBody struct {
	Model  string `json:"model"`
	Prompt string `json:"prompt"`
	// Format string `json:"format"`
	Stream bool `json:"stream"`
}

func main() {
	url := "http://localhost:11434/api/generate"

	// 创建请求数据
	requestBody := RequestBody{
		Model:  "llama3",
		Prompt: "Why is the sky blue?",
		// Prompt: "What color is the sky at different times of the day? Respond using JSON",
		// Format: "json",
		Stream: false,
	}

	// 将请求数据编码为 JSON
	jsonData, err := json.Marshal(requestBody)
	if err != nil {
		log.Fatalf("Error marshalling JSON: %v", err)
	}

	// 创建 POST 请求
	req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
	if err != nil {
		log.Fatalf("Error creating request: %v", err)
	}
	req.Header.Set("Content-Type", "application/json")

	// 发送请求
	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		log.Fatalf("Error sending request: %v", err)
	}
	defer resp.Body.Close()

	// 读取响应
	body, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Fatalf("Error reading response body: %v", err)
	}

	// 打印响应
	fmt.Println("Response Status:", resp.Status)
	fmt.Println("Response Body:", string(body))
}
