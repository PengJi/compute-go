package config

import (
	"log"
	"path/filepath"
	"runtime"

	"github.com/spf13/viper"
)

type Config struct {
	App struct {
		Name    string `mapstructure:"name"`
		Version string `mapstructure:"version"`
	} `mapstructure:"app"`
	Server struct {
		Port int `mapstructure:"port"`
	} `mapstructure:"server"`
	Log struct {
		Level string `mapstructure:"level"`
		File  string `mapstructure:"file"`
	} `mapstructure:"log"`
	Database struct {
		User     string `mapstructure:"user"`
		Password string `mapstructure:"password"`
		Host     string `mapstructure:"host"`
		Port     int    `mapstructure:"port"`
	} `mapstructure:"database"`
	Apilimit struct {
		Limit int `mapstructure:"limit"`
	} `mapstructure:"apilimit"`
}

var AppConfig Config

func LoadConfig() {
	// 获取当前文件的路径
	_, filePath, _, ok := runtime.Caller(0)
	if !ok {
		log.Fatalf("Error retrieving current file path")
	}

	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	// viper.AddConfigPath("./config/")
	viper.AddConfigPath(filepath.Dir(filePath))

	if err := viper.ReadInConfig(); err != nil {
		log.Fatalf("Error reading config file, %s", err)
	}

	if err := viper.Unmarshal(&AppConfig); err != nil {
		log.Fatalf("Unable to decode into struct, %v", err)
	}
}
