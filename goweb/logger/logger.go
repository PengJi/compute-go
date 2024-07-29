package logger

import (
	"context"
	"os"
	"strings"

	"golang.org/x/exp/slog"

	"goweb/config"
)

// LogLevel type
type LogLevel int

const (
	DebugLevel LogLevel = iota
	InfoLevel
	WarnLevel
	ErrorLevel
)

// Convert string level to LogLevel
func parseLogLevel(level string) LogLevel {
	switch strings.ToUpper(level) {
	case "DEBUG":
		return DebugLevel
	case "WARN":
		return WarnLevel
	case "ERROR":
		return ErrorLevel
	default:
		return InfoLevel
	}
}

type levelHandler struct {
	handler slog.Handler
	level   LogLevel
}

func (h *levelHandler) Enabled(ctx context.Context, level slog.Level) bool {
	var slogLevel LogLevel
	switch level {
	case slog.LevelDebug:
		slogLevel = DebugLevel
	case slog.LevelWarn:
		slogLevel = WarnLevel
	case slog.LevelError:
		slogLevel = ErrorLevel
	default:
		slogLevel = InfoLevel
	}
	return slogLevel >= h.level
}

func (h *levelHandler) Handle(ctx context.Context, r slog.Record) error {
	return h.handler.Handle(ctx, r)
}

func (h *levelHandler) WithAttrs(attrs []slog.Attr) slog.Handler {
	return &levelHandler{handler: h.handler.WithAttrs(attrs), level: h.level}
}

func (h *levelHandler) WithGroup(name string) slog.Handler {
	return &levelHandler{handler: h.handler.WithGroup(name), level: h.level}
}

var log *slog.Logger

func init() {
	config.LoadConfig()

	// 打开或创建一个日志文件
	file, err := os.OpenFile(config.AppConfig.Log.File, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		panic(err)
	}

	// 创建一个新的 JSON 格式的日志处理器
	handler := slog.NewJSONHandler(file, &slog.HandlerOptions{Level: slog.LevelInfo, AddSource: true})

	// 包装处理器以支持日志级别过滤
	level := parseLogLevel(config.AppConfig.Log.Level)
	levelHandler := &levelHandler{handler: handler, level: level}

	// 创建全局的日志记录器
	log = slog.New(levelHandler)
}

// GetLogger 返回全局的日志记录器
func GetLogger() *slog.Logger {
	return log
}
