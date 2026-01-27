#!/bin/bash
# Cursor MCP 天气服务器配置脚本

set -e

echo "🚀 配置 Cursor MCP 天气服务器"
echo "=" * 50

# 检查 Cursor 配置文件位置
echo "🔍 查找 Cursor 配置文件..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Cursor/User/globalStorage"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CONFIG_DIR="$HOME/.config/Cursor/User/globalStorage"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    CONFIG_DIR="$APPDATA/Cursor/User/globalStorage"
else
    echo "❌ 不支持的操作系统: $OSTYPE"
    exit 1
fi

CONFIG_FILE="$CONFIG_DIR/storage.json"

echo "配置文件位置: $CONFIG_FILE"

# 检查文件是否存在
if [ ! -f "$CONFIG_FILE" ]; then
    echo "⚠️  配置文件不存在，将创建新文件"
    mkdir -p "$CONFIG_DIR"
    echo '{}' > "$CONFIG_FILE"
fi

# 备份原配置
BACKUP_FILE="$CONFIG_FILE.backup.$(date +%Y%m%d_%H%M%S)"
cp "$CONFIG_FILE" "$BACKUP_FILE"
echo "✅ 已备份原配置到: $BACKUP_FILE"

# 读取当前配置
CURRENT_CONFIG=$(cat "$CONFIG_FILE")

# 创建新配置
echo "🔧 创建 MCP 服务器配置..."
NEW_CONFIG=$(python3 -c "
import json
import sys

try:
    config = json.loads('''$CURRENT_CONFIG''')
except:
    config = {}

# 确保 mcpServers 存在
if 'mcpServers' not in config:
    config['mcpServers'] = {}

# 添加天气服务器配置
config['mcpServers']['weather'] = {
    'command': 'python',
    'args': ['/home/jipeng/compute-go/agent/mcp/server.py', '--stdio'],
    'env': {},
    'description': '实时天气查询服务器（open-meteo）'
}

print(json.dumps(config, indent=2))
")

# 写入新配置
echo "$NEW_CONFIG" > "$CONFIG_FILE"
echo "✅ 配置已更新"

# 测试服务器
echo "🧪 测试服务器..."
cd /home/jipeng/compute-go/agent/mcp
if python -c "import sys; sys.path.insert(0, '.'); from weather_server import WeatherServer; print('✅ 服务器模块导入成功')"; then
    echo "✅ 服务器模块测试通过"
else
    echo "❌ 服务器模块测试失败"
    exit 1
fi

echo ""
echo "🎉 配置完成！"
echo ""
echo "下一步："
echo "1. 重启 Cursor"
echo "2. 在聊天中测试：@weather 今天北京天气怎么样？"
echo "3. 或者直接询问天气信息"
echo ""
echo "如果遇到问题："
echo "1. 查看 Cursor 开发者工具控制台（Help → Toggle Developer Tools）"
echo "2. 检查日志文件：/home/jipeng/compute-go/agent/mcp/weather_mcp.log"
echo "3. 运行测试：cd /home/jipeng/compute-go/agent/mcp && python test_client.py"
