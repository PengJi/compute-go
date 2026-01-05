#!/usr/bin/env python3
"""
直接测试天气服务器功能

这个测试直接调用 WeatherServer 类，不通过 MCP 协议。
"""

import asyncio
import os
from weather_server import WeatherServer


async def test_direct():
    """直接测试天气服务器"""
    print("🔧 直接测试天气服务器功能...")
    print()
    
    # 无需 API 密钥，使用 open-meteo 免费 API
    pass
    
    server = WeatherServer()
    
    try:
        # 测试 1: 搜索城市
        print("🔍 测试 1: 搜索城市 '杭州'")
        search_result = await server.search_city("杭州", "zh")
        print("搜索结果:")
        print(search_result)
        print()
        
        # 测试 2: 获取当前天气
        print("🌤️ 测试 2: 获取杭州当前天气")
        weather_result = await server.get_current_weather("杭州", "zh")
        print("天气信息:")
        print(weather_result)
        print()
        
        # 测试 3: 获取天气预报
        print("📅 测试 3: 获取杭州3天天气预报")
        forecast_result = await server.get_weather_forecast("杭州", 3, "zh")
        print("天气预报:")
        print(forecast_result)
        print()
        
        # 测试 4: 测试工具调用处理
        print("🛠️ 测试 4: 测试工具调用处理")
        tool_result = await server.handle_tool_call(
            "get_current_weather",
            {"city": "北京", "language": "zh"}
        )
        print("工具调用结果:")
        print(f"内容: {tool_result.content[0].text}")
        print(f"是否有错误: {tool_result.isError}")
        print()
        
        print("✅ 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await server.close()


if __name__ == "__main__":
    asyncio.run(test_direct())
