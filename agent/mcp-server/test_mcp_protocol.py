#!/usr/bin/env python3
"""
测试 MCP 协议实现
"""

import subprocess
import json
import time

def test_mcp_initialization():
    """测试 MCP 初始化协议"""
    print("🧪 测试 MCP 协议初始化")
    print("=" * 50)
    
    # 启动服务器进程
    print("1. 启动 MCP 服务器...")
    server_process = subprocess.Popen(
        ["python", "weather_server.py", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    # 给服务器一点时间启动
    time.sleep(0.5)
    
    try:
        # 发送初始化请求
        print("2. 发送初始化请求...")
        init_msg = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        server_process.stdin.write(json.dumps(init_msg) + "\n")
        server_process.stdin.flush()
        
        # 读取响应
        response = server_process.stdout.readline().strip()
        print(f"   初始化响应: {response[:100]}...")
        
        # 发送初始化完成通知
        print("3. 发送初始化完成通知...")
        initialized_msg = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        server_process.stdin.write(json.dumps(initialized_msg) + "\n")
        server_process.stdin.flush()
        
        # 测试工具列表
        print("4. 测试工具列表...")
        tools_msg = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        server_process.stdin.write(json.dumps(tools_msg) + "\n")
        server_process.stdin.flush()
        
        response = server_process.stdout.readline().strip()
        data = json.loads(response)
        tools = [tool["name"] for tool in data["result"]["tools"]]
        print(f"   可用工具: {tools}")
        
        # 测试工具调用
        print("5. 测试工具调用...")
        call_msg = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_current_weather",
                "arguments": {"city": "北京"}
            }
        }
        
        server_process.stdin.write(json.dumps(call_msg) + "\n")
        server_process.stdin.flush()
        
        response = server_process.stdout.readline().strip()
        data = json.loads(response)
        if data["result"]["content"]:
            text = data["result"]["content"][0]["text"]
            first_line = text.split('\n')[0]
            print(f"   天气查询结果: {first_line}")
        
        print("✅ MCP 协议测试通过！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        
        # 读取错误输出
        stderr_output = server_process.stderr.read()
        if stderr_output:
            print(f"服务器错误输出:\n{stderr_output}")
    finally:
        # 关闭服务器
        print("6. 关闭服务器...")
        server_process.terminate()
        server_process.wait()
        print("   服务器已关闭")

def test_with_mcp_client():
    """使用 MCP 客户端库测试"""
    print("\n🔧 使用 MCP 客户端库测试")
    print("=" * 50)
    
    try:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        import asyncio
        
        async def run_test():
            server_params = StdioServerParameters(
                command="python",
                args=["weather_server.py", "--stdio"],
                env=None
            )
            
            try:
                async with stdio_client(server_params) as (read_stream, write_stream):
                    async with ClientSession(read_stream, write_stream) as session:
                        # 初始化会话
                        print("1. 初始化 MCP 会话...")
                        await session.initialize()
                        print("   ✅ 初始化成功")
                        
                        # 获取工具列表
                        print("2. 获取工具列表...")
                        tools_result = await session.list_tools()
                        tools = [tool.name for tool in tools_result.tools]
                        print(f"   ✅ 工具列表: {tools}")
                        
                        # 调用工具
                        print("3. 调用天气查询工具...")
                        weather_result = await session.call_tool(
                            "get_current_weather",
                            {"city": "上海"}
                        )
                        print(f"   ✅ 工具调用成功")
                        if weather_result.content:
                            content = weather_result.content[0]
                            if hasattr(content, 'text'):
                                first_line = content.text.split('\n')[0]
                                print(f"   结果: {first_line}")
                        
                        print("✅ MCP 客户端测试通过！")
                        
            except Exception as e:
                print(f"❌ MCP 客户端测试失败: {e}")
                import traceback
                traceback.print_exc()
        
        asyncio.run(run_test())
        
    except ImportError as e:
        print(f"⚠️  无法导入 MCP 客户端库: {e}")
        print("   请安装依赖: pip install mcp")

def main():
    """主函数"""
    print("MCP 协议兼容性测试")
    print("=" * 50)
    
    test_mcp_initialization()
    test_with_mcp_client()
    
    print("\n" + "=" * 50)
    print("测试完成！")

if __name__ == "__main__":
    main()
