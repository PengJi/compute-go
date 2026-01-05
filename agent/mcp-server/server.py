#!/usr/bin/env python3
"""
MCP 天气服务器 - 包装器

这个文件是 weather_server.py 的包装器，提供更好的日志和错误处理。
实际 MCP 服务器实现在 weather_server.py 中。
"""

import sys
import os

if __name__ == "__main__":
    # 检查是否以 stdio 模式运行
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # stdio 模式 - 直接调用 weather_server.py
        import subprocess
        import signal
        
        def signal_handler(signum, frame):
            print(f"收到信号 {signum}，退出", file=sys.stderr)
            sys.exit(0)
        
        # 设置信号处理
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # 启动 weather_server.py
        print("🚀 启动 MCP 天气服务器...", file=sys.stderr)
        print(f"📁 工作目录: {os.getcwd()}", file=sys.stderr)
        print(f"🐍 Python 路径: {sys.executable}", file=sys.stderr)
        print("=" * 50, file=sys.stderr)
        
        try:
            # 直接运行 weather_server.py
            import weather_server
            import asyncio
            asyncio.run(weather_server.main())
        except KeyboardInterrupt:
            print("\n服务器被中断", file=sys.stderr)
            sys.exit(0)
        except Exception as e:
            print(f"服务器错误: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)
            sys.exit(1)
            
    else:
        # 独立运行模式 - 显示帮助信息
        print("MCP 天气服务器包装器")
        print("=" * 50)
        print()
        print("这个文件包装了 weather_server.py，提供更好的日志和错误处理。")
        print()
        print("特点:")
        print("✅ 无需 API 密钥")
        print("✅ 支持 41 个全球主要城市")
        print("✅ 使用 open-meteo 免费天气 API")
        print("✅ 提供当前天气和天气预报")
        print()
        print("使用方法:")
        print("1. 作为 MCP 服务器运行:")
        print("   python server.py --stdio")
        print()
        print("2. 直接运行 weather_server.py:")
        print("   python weather_server.py --stdio")
        print()
        print("3. 运行测试:")
        print("   python test_client.py")
        print()
        print("4. 查看支持的城市:")
        print("   python -c \"from weather_server import CITY_COORDINATES; print('支持的城市:', ', '.join(sorted(CITY_COORDINATES.keys())[:20]))\"")
        print()
        sys.exit(0)