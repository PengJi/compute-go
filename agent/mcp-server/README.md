# MCP 天气服务器（open-meteo 版本）

一个基于 Model Context Protocol (MCP) 的实时天气查询服务器，使用 open-meteo 免费天气 API，无需 API 密钥。

## 🌤️ 功能特性

- **实时天气查询**: 获取指定城市的当前天气状况
- **天气预报**: 提供1-7天的天气预报
- **城市搜索**: 支持城市名称搜索和自动补全
- **多语言支持**: 支持中文和英文
- **无需API密钥**: 使用免费的 open-meteo API
- **支持41个城市**: 包括中国主要城市和国际城市
- **错误处理**: 完善的错误处理和用户提示

## 🚀 快速开始

### 前提条件

- Python 3.8 或更高版本
- **无需 API 密钥** - 完全免费使用

### 安装步骤

1. **克隆或下载项目**
   ```bash
   cd /home/jipeng/compute-go/agent/mcp
   ```

2. **运行安装脚本**
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

3. **查看支持的城市**
   ```bash
   # 查看所有支持的城市
   python -c "from weather_server import CITY_COORDINATES; print('支持的城市:', ', '.join(sorted(CITY_COORDINATES.keys())))"
   
   # 或运行测试查看
   python test_client.py
   ```

5. **测试安装**
   ```bash
   ./test.sh
   ```

## 📖 使用方法

### 作为 MCP 服务器运行

MCP 服务器可以通过 stdio 模式运行，供支持 MCP 协议的客户端调用：

```bash
# 启动 MCP 服务器
./start_server.sh --stdio
```

### 测试工具

项目提供了测试客户端，可以交互式测试所有功能：

```bash
# 运行测试客户端
./test.sh
```

### 交互式命令

在测试客户端中可以使用以下命令：

```
tools              - 查看可用工具
search <城市>      - 搜索城市
weather <城市>     - 获取当前天气
forecast <城市> [天数] - 获取天气预报
help               - 显示帮助
quit               - 退出
```

## 🔧 工具说明

### 1. get_current_weather
获取指定城市的当前天气状况。

**参数:**
- `city` (必填): 城市名称，例如："北京"、"上海"、"杭州"
- `language` (可选): 返回语言，zh（中文）或 en（英文），默认为 zh

**示例:**
```json
{
  "city": "杭州",
  "language": "zh"
}
```

### 2. get_weather_forecast
获取指定城市的天气预报。

**参数:**
- `city` (必填): 城市名称
- `days` (可选): 预报天数，1-7，默认为 3
- `language` (可选): 返回语言，默认为 zh

**示例:**
```json
{
  "city": "北京",
  "days": 5,
  "language": "zh"
}
```

### 3. search_city
搜索城市，获取城市ID用于精确查询。

**参数:**
- `keyword` (必填): 搜索关键词，可以是城市名称、拼音或英文名
- `language` (可选): 返回语言，默认为 zh

**示例:**
```json
{
  "keyword": "hangzhou",
  "language": "en"
}
```

## 🏗️ 项目结构

```
mcp/
├── weather_server.py     # 天气服务核心逻辑
├── server.py            # MCP 服务器主文件
├── test_client.py       # 测试客户端
├── config.yaml          # 配置文件
├── requirements.txt     # Python 依赖
├── install.sh          # 安装脚本
├── start_server.sh     # 启动脚本
├── test.sh            # 测试脚本
└── README.md          # 本文档
```

## ⚙️ 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `LOG_LEVEL` | 日志级别 | INFO |
| `CACHE_ENABLED` | 是否启用缓存 | true |

### 配置文件

`config.yaml` 包含完整的服务器配置：

```yaml
# 服务器配置
server:
  name: "weather-mcp-server"
  version: "1.0.0"
  description: "基于 open-meteo API 的天气查询服务器"
  
# open-meteo API 配置
open_meteo:
  base_url: "https://api.open-meteo.com/v1/forecast"
  
# 缓存配置
cache:
  enabled: true
  city_cache_ttl: 3600    # 城市坐标缓存时间（秒）
  weather_cache_ttl: 300  # 天气数据缓存时间（秒）
  
# 城市数据库
cities:
  total_supported: 41
  include_china_major: true
  include_international: true
```

## 🔌 集成到 MCP 客户端

### 在 Claude Desktop 中使用

1. 编辑 Claude Desktop 的配置文件（通常位于 `~/Library/Application Support/Claude/claude_desktop_config.json`）

2. 添加 MCP 服务器配置：

```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": ["/path/to/compute-go/agent/mcp/server.py", "--stdio"],
      "env": {}
    }
  }
}
```

### 在 Cursor 中使用

1. 在 Cursor 设置中添加 MCP 服务器配置
2. 使用与 Claude Desktop 类似的配置

## 🐛 故障排除

### 常见问题

1. **城市找不到**
   ```
   错误: 未找到城市 'xxx' 的坐标信息
   ```
   **解决方案**: 
   - 使用 `search_city` 工具搜索城市
   - 查看支持的城市列表
   - 确保使用正确的中文名称或拼音

2. **网络连接问题**
   ```
   错误: API请求失败: ...
   ```
   **解决方案**: 
   - 检查网络连接
   - 确保可以访问 open-meteo API (https://api.open-meteo.com)
   - 等待一段时间后重试

3. **数据不完整**
   ```
   备注: 免费API，数据可能有限
   ```
   **解决方案**: 
   - 这是正常现象，open-meteo 免费版提供基本天气数据
   - 如需更详细数据，可考虑使用其他天气 API

### 日志查看

服务器日志保存在 `weather_mcp.log` 文件中：

```bash
tail -f weather_mcp.log
```

## 📊 服务特点

- **完全免费**: 使用 open-meteo 免费天气 API，无调用限制
- **无需注册**: 无需 API 密钥，开箱即用
- **全球覆盖**: 支持全球主要城市的天气查询
- **实时数据**: 提供最新的天气信息和预报

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。

## 🙏 致谢

- [open-meteo](https://open-meteo.com/) - 提供免费的天气数据 API
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP 协议
- 所有贡献者和用户

## 📞 支持

如有问题或建议，请：
1. 查看 [常见问题](#常见问题)
2. 提交 [Issue](https://github.com/your-repo/issues)
3. 联系维护者

---

**Happy Coding!** 🚀
