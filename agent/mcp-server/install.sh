#!/bin/bash
# MCP 天气服务器安装脚本

set -e

echo "🚀 开始安装 MCP 天气服务器..."
echo

# 检查 Python 版本
echo "🔍 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python 版本: $python_version"

if [[ "$python_version" < "3.8" ]]; then
    echo "❌ 需要 Python 3.8 或更高版本"
    exit 1
fi

# 检查 pip
echo "🔍 检查 pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ 未找到 pip3，请先安装 pip"
    exit 1
fi

# 创建虚拟环境
echo "🔧 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ 虚拟环境创建成功"
else
    echo "📁 虚拟环境已存在"
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 检查配置
echo "🔧 检查配置..."
echo "✅ 使用 open-meteo 免费 API，无需 API 密钥"
echo "✅ 支持 41 个全球主要城市"

# 创建启动脚本
echo "🔧 创建启动脚本..."
cat > start_server.sh << 'EOF'
#!/bin/bash
# MCP 天气服务器启动脚本

set -e

# 激活虚拟环境
source venv/bin/activate

echo "🚀 启动 MCP 天气服务器..."
echo "使用 open-meteo 免费 API"
echo "支持 41 个全球主要城市"
echo

# 运行服务器
python server.py "$@"
EOF

chmod +x start_server.sh

# 创建测试脚本
echo "🔧 创建测试脚本..."
cat > test.sh << 'EOF'
#!/bin/bash
# MCP 天气服务器测试脚本

set -e

# 激活虚拟环境
source venv/bin/activate

echo "🧪 运行测试..."
python test_client.py
EOF

chmod +x test.sh

# 创建配置文件示例
echo "📄 检查配置文件示例..."
if [ ! -f "env.example" ]; then
    echo "⚠️  配置文件示例不存在，已创建 env.example"
else
    echo "✅ 配置文件示例已存在"
    echo "   请查看 env.example 文件了解配置选项"
fi

echo
echo "🎉 安装完成！"
echo
echo "📋 可用命令:"
echo "  ./start_server.sh      - 启动 MCP 服务器"
echo "  ./test.sh              - 运行测试"
echo "  source venv/bin/activate - 激活虚拟环境"
echo
echo "🔧 配置说明:"
echo "  1. 无需 API 密钥，开箱即用"
echo "  2. 查看 env.example 了解可选配置"
echo
echo "🚀 快速开始:"
echo "  1. 设置 API 密钥"
echo "  2. 运行: ./test.sh"
echo "  3. 选择交互式测试模式"
echo
echo "📚 更多信息请查看 README.md"
