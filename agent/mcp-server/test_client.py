#!/usr/bin/env python3
"""
MCP 天气服务器测试客户端

用于测试 MCP 服务器的功能。
"""

import asyncio
import json
import sys
from typing import Dict, Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_weather_server():
    """测试天气服务器"""
    print("🔧 测试天气服务器功能...")
    print("注意: 使用直接测试模式，避免 MCP 协议循环问题")
    print()
    
    # 直接测试 WeatherServer 类，不通过 MCP 协议
    from weather_server import WeatherServer
    
    server = WeatherServer()
    
    try:
        # 测试 1: 搜索城市
        print("🔍 测试 1: 搜索城市 '杭州'")
        search_result = await server.search_city("杭州")
        print("搜索结果:")
        if "error" in search_result:
            print(f"错误: {search_result['error']}")
        else:
            print(f"找到 {search_result['total_results']} 个结果")
            for city in search_result["cities"]:
                print(f"  - {city['name']} ({city['latitude']}, {city['longitude']})")
        print()
        
        # 测试 2: 获取当前天气
        print("🌤️ 测试 2: 获取杭州当前天气")
        weather_result = await server.get_current_weather("杭州")
        print("天气信息:")
        if "error" in weather_result:
            print(f"错误: {weather_result['error']}")
        else:
            print(f"城市: {weather_result['city']}")
            print(f"温度: {weather_result['temperature']}")
            print(f"天气: {weather_result['weather']}")
            print(f"风向: {weather_result['wind_direction']} {weather_result['wind_speed']}")
            print(f"更新时间: {weather_result['update_time']}")
        print()
        
        # 测试 3: 获取天气预报
        print("📅 测试 3: 获取杭州3天天气预报")
        forecast_result = await server.get_weather_forecast("杭州", 3)
        print("天气预报:")
        if "error" in forecast_result:
            print(f"错误: {forecast_result['error']}")
        else:
            print(f"城市: {forecast_result['city']}")
            print(f"预报天数: {forecast_result['forecast_days']}")
            for forecast in forecast_result["forecasts"]:
                print(f"  {forecast['date']}: {forecast['weather']}, {forecast['min_temp']}~{forecast['max_temp']}")
        print()
        
        # 测试 4: 测试工具调用处理
        print("🛠️ 测试 4: 测试工具调用处理")
        tool_result = await server.handle_tool_call(
            "get_current_weather",
            {"city": "北京"}
        )
        print("工具调用结果:")
        print(f"是否有错误: {tool_result.isError}")
        if tool_result.content:
            for content in tool_result.content:
                if hasattr(content, 'text'):
                    print("返回内容:")
                    print(content.text)
        print()
        
        # 测试 5: 测试错误情况
        print("⚠️ 测试 5: 测试不存在的城市")
        error_result = await server.get_current_weather("不存在的城市123")
        print("错误响应:")
        if "error" in error_result:
            print(f"错误: {error_result['error']}")
            if "suggestion" in error_result:
                print(f"建议: {error_result['suggestion']}")
        print()
        
        print("✅ 所有测试完成！")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await server.close()


async def interactive_test():
    """交互式测试"""
    print("🎮 天气服务器交互式测试")
    print("输入 'quit' 退出")
    print("输入 'help' 查看帮助")
    print("=" * 50)
    
    # 直接使用 WeatherServer 类
    from weather_server import WeatherServer
    
    server = WeatherServer()
    
    try:
        print("\n可用命令:")
        print("1. tools - 查看可用工具")
        print("2. search <城市> - 搜索城市")
        print("3. weather <城市> - 获取当前天气")
        print("4. forecast <城市> [天数] - 获取天气预报")
        print("5. cities - 查看支持的城市")
        print("6. help - 显示帮助")
        print("7. quit - 退出")
        print()
        
        while True:
            try:
                command = input("> ").strip()
                
                if command.lower() in ['quit', 'exit', 'q']:
                    print("再见！👋")
                    break
                
                elif command.lower() in ['help', '?']:
                    print("\n可用命令:")
                    print("1. tools - 查看可用工具")
                    print("2. search <城市> - 搜索城市")
                    print("3. weather <城市> - 获取当前天气")
                    print("4. forecast <城市> [天数] - 获取天气预报")
                    print("5. cities - 查看支持的城市")
                    print("6. help - 显示帮助")
                    print("7. quit - 退出")
                    print()
                
                elif command.lower() == 'tools':
                    print("\n可用工具:")
                    print("1. get_current_weather - 获取当前天气")
                    print("   参数: city (城市名称), language (语言，默认zh)")
                    print()
                    print("2. get_weather_forecast - 获取天气预报")
                    print("   参数: city (城市名称), days (天数，默认3), language (语言，默认zh)")
                    print()
                    print("3. search_city - 搜索城市")
                    print("   参数: keyword (搜索关键词), language (语言，默认zh)")
                    print()
                
                elif command.lower() == 'cities':
                    from weather_server import CITY_COORDINATES
                    print(f"\n支持的城市 (共 {len(CITY_COORDINATES)} 个):")
                    cities = sorted(CITY_COORDINATES.keys())
                    for i in range(0, len(cities), 8):
                        print("  " + ", ".join(cities[i:i+8]))
                    print()
                
                elif command.startswith('search '):
                    keyword = command[7:].strip()
                    if keyword:
                        print(f"\n搜索城市: {keyword}")
                        result = await server.search_city(keyword)
                        if "error" in result:
                            print(f"错误: {result['error']}")
                        else:
                            print(f"找到 {result['total_results']} 个结果:")
                            for city in result["cities"]:
                                print(f"  - {city['name']} ({city['latitude']}, {city['longitude']})")
                    else:
                        print("请输入搜索关键词")
                    print()
                
                elif command.startswith('weather '):
                    city = command[8:].strip()
                    if city:
                        print(f"\n获取 {city} 的天气...")
                        result = await server.get_current_weather(city)
                        if "error" in result:
                            print(f"错误: {result['error']}")
                            if "suggestion" in result:
                                print(f"建议: {result['suggestion']}")
                        else:
                            print(f"🌤️ {result['city']} 当前天气")
                            print(f"温度: {result['temperature']}")
                            print(f"天气: {result['weather']}")
                            print(f"风向: {result['wind_direction']} {result['wind_speed']}")
                            print(f"更新时间: {result['update_time']}")
                    else:
                        print("请输入城市名称")
                    print()
                
                elif command.startswith('forecast '):
                    parts = command[9:].strip().split()
                    if len(parts) >= 1:
                        city = parts[0]
                        days = int(parts[1]) if len(parts) > 1 else 3
                        days = max(1, min(days, 7))  # 限制在1-7天
                        print(f"\n获取 {city} 的 {days} 天天气预报...")
                        result = await server.get_weather_forecast(city, days)
                        if "error" in result:
                            print(f"错误: {result['error']}")
                            if "suggestion" in result:
                                print(f"建议: {result['suggestion']}")
                        else:
                            print(f"📅 {result['city']} {days} 天天气预报")
                            for forecast in result["forecasts"]:
                                print(f"  {forecast['date']}: {forecast['weather']}, {forecast['min_temp']}~{forecast['max_temp']}, 降水: {forecast['precip']}")
                    else:
                        print("请输入城市名称")
                    print()
                
                else:
                    print("未知命令，输入 'help' 查看帮助")
                    print()
                    
            except KeyboardInterrupt:
                print("\n\n再见！👋")
                break
            except Exception as e:
                print(f"错误: {e}")
                print()
    
    finally:
        await server.close()


def main():
    """主函数"""
    print("MCP 天气服务器测试客户端")
    print("=" * 50)
    print()
    
    # 检查是否在非交互式环境中运行
    if not sys.stdin.isatty():
        # 非交互式环境，直接运行自动测试
        print("检测到非交互式环境，运行自动测试...")
        asyncio.run(test_weather_server())
        return
    
    print("选择测试模式:")
    print("1. 自动测试")
    print("2. 交互式测试")
    print("3. 退出")
    print()
    
    while True:
        try:
            choice = input("请选择 (1-3): ").strip()
            
            if choice == '1':
                asyncio.run(test_weather_server())
                break
            elif choice == '2':
                asyncio.run(interactive_test())
                break
            elif choice == '3':
                print("再见！👋")
                break
            else:
                print("无效选择，请重新输入")
        except (EOFError, KeyboardInterrupt):
            print("\n检测到中断，运行自动测试...")
            asyncio.run(test_weather_server())
            break


if __name__ == "__main__":
    print("MCP 天气服务器测试客户端（open-meteo 版本）")
    print("=" * 50)
    print()
    print("特点:")
    print("✅ 无需 API 密钥")
    print("✅ 使用 open-meteo 免费天气 API")
    print("✅ 支持中国主要城市和国际城市")
    print()
    
    main()
