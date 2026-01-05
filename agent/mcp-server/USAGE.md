# MCP 天气服务器使用指南

## 📋 目录

1. [安装与配置](#安装与配置)
2. [基本使用](#基本使用)
3. [工具详解](#工具详解)
4. [集成到AI助手](#集成到ai助手)
5. [高级配置](#高级配置)
6. [故障排除](#故障排除)

## 🛠️ 安装与配置

### 快速安装

```bash
# 进入项目目录
cd /home/jipeng/compute-go/agent/mcp

# 运行安装脚本
chmod +x install.sh
./install.sh
```

### 无需 API 密钥

本项目使用 open-meteo 免费天气 API，无需注册和 API 密钥：
- 完全免费使用
- 无调用次数限制
- 支持全球主要城市

### 查看支持的城市

```bash
# 查看所有支持的城市
python -c "from weather_server import CITY_COORDINATES; print('支持的城市:', ', '.join(sorted(CITY_COORDINATES.keys())))"

# 或运行测试查看
python test_client.py
```

## 🚀 基本使用

### 启动服务器

```bash
# 方法1：使用启动脚本
./start_server.sh --stdio

# 方法2：直接运行
source venv/bin/activate
python server.py --stdio
```

### 测试功能

```bash
# 运行测试客户端
./test.sh

# 或直接运行
python test_client.py
```

### 测试客户端界面

```
MCP 天气服务器测试客户端
==================================================

选择测试模式:
1. 自动测试
2. 交互式测试
3. 退出

请选择 (1-3): 2
```

## 🔧 工具详解

### 1. get_current_weather

获取指定城市的当前天气状况。

**示例请求:**
```json
{
  "city": "北京",
  "language": "zh"
}
```

**示例响应:**
```
🌤️ 北京 当前天气
温度: 15°C (体感 14°C)
天气: 晴
风向: 北风 2级 (7 km/h)
湿度: 45%
气压: 1013 hPa
能见度: 10 km
云量: 20%
更新时间: 2024-01-04 14:30:00
```

### 2. get_weather_forecast

获取指定城市的天气预报。

**示例请求:**
```json
{
  "city": "上海",
  "days": 3,
  "language": "zh"
}
```

**示例响应:**
```
🌤️ 上海 3天天气预报

📅 2024-01-04:
  白天: 多云
  夜间: 阴
  温度: 8°C ~ 12°C
  日出: 06:45, 日落: 17:15

📅 2024-01-05:
  白天: 小雨
  夜间: 阴
  温度: 7°C ~ 11°C
  日出: 06:45, 日落: 17:16

📅 2024-01-06:
  白天: 阴
  夜间: 多云
  温度: 6°C ~ 10°C
  日出: 06:45, 日落: 17:17

更新时间: 2024-01-04T14:30:00+08:00
```

### 3. search_city

搜索城市，获取城市ID。

**示例请求:**
```json
{
  "keyword": "hangzhou",
  "language": "en"
}
```

**示例响应:**
```
🔍 搜索 'hangzhou' 找到 1 个结果:

1. Hangzhou (Zhejiang, China)
   ID: 101210101
   坐标: 30.27415, 120.15515
   时区: Asia/Shanghai
```

## 🤖 集成到AI助手

### Claude Desktop 集成

1. 找到 Claude Desktop 配置文件：
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/Claude/claude_desktop_config.json`

2. 编辑配置文件：
```json
{
  "mcpServers": {
    "weather": {
      "command": "python",
      "args": [
        "/home/jipeng/compute-go/agent/mcp/server.py",
        "--stdio"
      ],
      "env": {}
    }
  }
}
```

3. 重启 Claude Desktop

### Cursor 集成

1. 打开 Cursor 设置
2. 找到 MCP 服务器配置
3. 添加新服务器：
   - **名称**: weather
   - **命令**: python
   - **参数**: `/home/jipeng/compute-go/agent/mcp/server.py --stdio`
   - **无需 API 密钥**: 使用 open-meteo 免费 API

### 在对话中使用

集成后，AI助手会自动使用天气工具：

```
用户：今天北京天气怎么样？

AI助手：让我查一下北京的天气...
[调用 get_current_weather 工具]
北京今天天气晴朗，温度15°C，体感温度14°C，北风2级...
```

## ⚙️ 高级配置

### 修改缓存设置

编辑 `config.yaml`：

```yaml
cache:
  city_cache_ttl: 7200      # 城市ID缓存2小时
  weather_cache_ttl: 600    # 天气数据缓存10分钟
```

### 启用详细日志

```bash
# 设置环境变量
export LOG_LEVEL=DEBUG

# 或编辑 config.yaml
server:
  log_level: "DEBUG"
```

### 自定义默认城市

在 `config.yaml` 中添加更多默认城市：

```yaml
default_cities:
  - name: "成都"
    id: "101270101"
  - name: "重庆"
    id: "101040100"
  - name: "武汉"
    id: "101200101"
```

## 🐛 故障排除

### 常见错误

1. **API 密钥无效**
   ```
   错误: 获取天气数据失败: 无效的API密钥
   ```
   **解决**: 检查 API 密钥是否正确，确保已激活

2. **城市找不到**
   ```
   错误: 未找到城市 'xxx' 的信息
   ```
   **解决**: 先用 `search_city` 工具确认城市名称

3. **网络连接失败**
   ```
   错误: HTTP请求失败: ...
   ```
   **解决**: 
   - 检查网络连接
   - 确认可以访问 `devapi.qweather.com`
   - 尝试使用代理

### 查看日志

```bash
# 实时查看日志
tail -f weather_mcp.log

# 查看错误日志
grep ERROR weather_mcp.log

# 查看最近100行
tail -n 100 weather_mcp.log
```

### 调试模式

```bash
# 启用调试
export DEBUG=true
export LOG_LEVEL=DEBUG

# 重新启动服务器
./start_server.sh --stdio
```

## 📊 性能优化

### 启用缓存

缓存可以显著减少 API 调用：

```bash
# 确保缓存已启用
export CACHE_ENABLED=true
```

### 调整缓存时间

根据使用频率调整缓存时间：

```yaml
# 高频查询城市
cache:
  city_cache_ttl: 86400    # 24小时
  weather_cache_ttl: 900   # 15分钟
```

### 监控 API 使用

open-meteo API 使用情况：
- 免费使用，无调用次数限制
- 提供基本天气数据
- 如需更详细数据可考虑其他天气 API

## 🔄 更新与维护

### 更新依赖

```bash
# 激活虚拟环境
source venv/bin/activate

# 更新所有依赖
pip install --upgrade -r requirements.txt
```

### 备份配置

```bash
# 备份重要文件
cp config.yaml config.yaml.backup
cp .env .env.backup
```

### 恢复安装

如果遇到问题，可以重新安装：

```bash
# 删除虚拟环境
rm -rf venv

# 重新安装
./install.sh
```

## 📞 获取帮助

### 查看文档
- `README.md` - 项目概述
- `USAGE.md` - 本使用指南
- 代码中的文档字符串

### 报告问题

遇到问题时，请提供：
1. 错误信息
2. 复现步骤
3. 日志文件内容
4. 系统环境信息

### 社区支持

- GitHub Issues
- 项目讨论区
- 开发者社区

---

**祝您使用愉快！** 🌤️

如果有任何问题或建议，欢迎反馈！
