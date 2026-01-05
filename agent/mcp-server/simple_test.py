#!/usr/bin/env python3
"""
简单测试脚本 - 直接测试 WeatherServer 功能

这个脚本直接测试 WeatherServer 类的功能，不通过 MCP 协议。
"""

import asyncio
from weather_server import WeatherServer


async def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试天气服务器基本功能")
    print("=" * 50)
    
    server = WeatherServer()
    
    try:
        # 测试搜索城市
        print("\n1. 测试搜索城市:")
        print("   搜索 '北京':")
        result = await server.search_city("北京")
        if "error" in result:
            print(f"   错误: {result['error']}")
        else:
            print(f"   找到 {result['total_results']} 个结果")
            for city in result["cities"][:3]:  # 显示前3个
                print(f"   - {city['name']} ({city['latitude']}, {city['longitude']})")
        
        print("\n   搜索 'beijing' (拼音):")
        result = await server.search_city("beijing")
        if "error" in result:
            print(f"   错误: {result['error']}")
        else:
            print(f"   找到 {result['total_results']} 个结果")
        
        # 测试当前天气
        print("\n2. 测试当前天气:")
        cities_to_test = ["北京", "上海", "杭州", "纽约"]
        for city in cities_to_test:
            print(f"\n   查询 {city}:")
            result = await server.get_current_weather(city)
            if "error" in result:
                print(f"   错误: {result['error']}")
            else:
                print(f"   温度: {result['temperature']}")
                print(f"   天气: {result['weather']}")
                print(f"   风向: {result['wind_direction']} {result['wind_speed']}")
                print(f"   来源: {result.get('source', '未知')}")
        
        # 测试天气预报
        print("\n3. 测试天气预报:")
        print("   查询北京3天预报:")
        result = await server.get_weather_forecast("北京", 3)
        if "error" in result:
            print(f"   错误: {result['error']}")
        else:
            print(f"   城市: {result['city']}")
            print(f"   天数: {result['forecast_days']}")
            for forecast in result["forecasts"]:
                print(f"   {forecast['date']}: {forecast['weather']}, {forecast['min_temp']}~{forecast['max_temp']}, 降水: {forecast['precip']}")
        
        # 测试工具调用处理
        print("\n4. 测试工具调用处理:")
        print("   测试 get_current_weather 工具:")
        tool_result = await server.handle_tool_call(
            "get_current_weather",
            {"city": "广州", "language": "zh"}
        )
        print(f"   结果: {'有错误' if tool_result.isError else '成功'}")
        if tool_result.content:
            content = tool_result.content[0]
            if hasattr(content, 'text'):
                # 只显示前几行
                lines = content.text.split('\n')[:5]
                for line in lines:
                    print(f"   {line}")
        
        print("\n✅ 所有测试完成！")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await server.close()


async def test_city_coverage():
    """测试城市覆盖"""
    print("\n🌍 测试城市覆盖")
    print("=" * 50)
    
    server = WeatherServer()
    
    try:
        # 从 weather_server 导入城市列表
        from weather_server import CITY_COORDINATES
        
        print(f"支持的城市数量: {len(CITY_COORDINATES)}")
        print("\n按地区分组:")
        
        # 分组显示
        china_cities = []
        international_cities = []
        
        for city in sorted(CITY_COORDINATES.keys()):
            if city in ['纽约', '伦敦', '东京', '巴黎', '悉尼', '新加坡']:
                international_cities.append(city)
            else:
                china_cities.append(city)
        
        print(f"\n中国城市 ({len(china_cities)} 个):")
        for i in range(0, len(china_cities), 8):
            print("  " + ", ".join(china_cities[i:i+8]))
        
        print(f"\n国际城市 ({len(international_cities)} 个):")
        print("  " + ", ".join(international_cities))
        
        # 测试几个随机城市
        print("\n随机测试几个城市:")
        test_cities = list(CITY_COORDINATES.keys())[:5]  # 前5个城市
        for city in test_cities:
            result = await server.get_current_weather(city)
            if "error" not in result:
                print(f"  {city}: {result['temperature']}, {result['weather']}")
            else:
                print(f"  {city}: 查询失败 - {result['error']}")
        
    finally:
        await server.close()


def main():
    """主函数"""
    print("MCP 天气服务器功能测试")
    print("=" * 50)
    
    # 运行测试
    asyncio.run(test_basic_functionality())
    asyncio.run(test_city_coverage())
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n使用说明:")
    print("1. 直接运行: python simple_test.py")
    print("2. 作为 MCP 服务器: python server.py --stdio")
    print("3. 交互测试: python test_client.py")


if __name__ == "__main__":
    main()
