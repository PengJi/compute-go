#!/usr/bin/env python3
"""
MCP Weather Server - 实时天气查询 MCP 服务器

这个 MCP 服务器提供实时天气查询功能，支持通过城市名称查询当前天气状况。
使用 open-meteo 免费天气 API 作为数据源，无需 API 密钥。
"""

import asyncio
import json
import os
import sys
from typing import Any, Dict, List, Optional
from datetime import datetime

import httpx
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)

# 配置
# 使用 open-meteo API (无需 API 密钥)
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# 城市坐标数据库（常见城市）
CITY_COORDINATES = {
    "北京": {"latitude": 39.9042, "longitude": 116.4074, "timezone": "Asia/Shanghai"},
    "上海": {"latitude": 31.2304, "longitude": 121.4737, "timezone": "Asia/Shanghai"},
    "广州": {"latitude": 23.1291, "longitude": 113.2644, "timezone": "Asia/Shanghai"},
    "深圳": {"latitude": 22.5431, "longitude": 114.0579, "timezone": "Asia/Shanghai"},
    "杭州": {"latitude": 30.2741, "longitude": 120.1552, "timezone": "Asia/Shanghai"},
    "成都": {"latitude": 30.5728, "longitude": 104.0668, "timezone": "Asia/Shanghai"},
    "重庆": {"latitude": 29.5630, "longitude": 106.5516, "timezone": "Asia/Shanghai"},
    "武汉": {"latitude": 30.5928, "longitude": 114.3055, "timezone": "Asia/Shanghai"},
    "西安": {"latitude": 34.3416, "longitude": 108.9398, "timezone": "Asia/Shanghai"},
    "南京": {"latitude": 32.0603, "longitude": 118.7969, "timezone": "Asia/Shanghai"},
    # 添加更多中国城市
    "天津": {"latitude": 39.3434, "longitude": 117.3616, "timezone": "Asia/Shanghai"},
    "沈阳": {"latitude": 41.8057, "longitude": 123.4315, "timezone": "Asia/Shanghai"},
    "哈尔滨": {"latitude": 45.8038, "longitude": 126.5340, "timezone": "Asia/Shanghai"},
    "长春": {"latitude": 43.8171, "longitude": 125.3235, "timezone": "Asia/Shanghai"},
    "大连": {"latitude": 38.9140, "longitude": 121.6147, "timezone": "Asia/Shanghai"},
    "济南": {"latitude": 36.6512, "longitude": 117.1201, "timezone": "Asia/Shanghai"},
    "青岛": {"latitude": 36.0671, "longitude": 120.3826, "timezone": "Asia/Shanghai"},
    "厦门": {"latitude": 24.4798, "longitude": 118.0894, "timezone": "Asia/Shanghai"},
    "福州": {"latitude": 26.0745, "longitude": 119.2965, "timezone": "Asia/Shanghai"},
    "长沙": {"latitude": 28.2282, "longitude": 112.9388, "timezone": "Asia/Shanghai"},
    "郑州": {"latitude": 34.7466, "longitude": 113.6253, "timezone": "Asia/Shanghai"},
    "合肥": {"latitude": 31.8206, "longitude": 117.2272, "timezone": "Asia/Shanghai"},
    "南昌": {"latitude": 28.6820, "longitude": 115.8579, "timezone": "Asia/Shanghai"},
    "昆明": {"latitude": 24.8801, "longitude": 102.8329, "timezone": "Asia/Shanghai"},
    "贵阳": {"latitude": 26.6477, "longitude": 106.6302, "timezone": "Asia/Shanghai"},
    "南宁": {"latitude": 22.8170, "longitude": 108.3665, "timezone": "Asia/Shanghai"},
    "海口": {"latitude": 20.0440, "longitude": 110.1983, "timezone": "Asia/Shanghai"},
    "兰州": {"latitude": 36.0611, "longitude": 103.8343, "timezone": "Asia/Shanghai"},
    "西宁": {"latitude": 36.6171, "longitude": 101.7782, "timezone": "Asia/Shanghai"},
    "银川": {"latitude": 38.4872, "longitude": 106.2309, "timezone": "Asia/Shanghai"},
    "乌鲁木齐": {"latitude": 43.8256, "longitude": 87.6168, "timezone": "Asia/Urumqi"},
    "拉萨": {"latitude": 29.6525, "longitude": 91.1721, "timezone": "Asia/Shanghai"},
    "香港": {"latitude": 22.3193, "longitude": 114.1694, "timezone": "Asia/Hong_Kong"},
    "澳门": {"latitude": 22.1987, "longitude": 113.5439, "timezone": "Asia/Macau"},
    "台北": {"latitude": 25.0330, "longitude": 121.5654, "timezone": "Asia/Taipei"},
    # 国际主要城市
    "纽约": {"latitude": 40.7128, "longitude": -74.0060, "timezone": "America/New_York"},
    "伦敦": {"latitude": 51.5074, "longitude": -0.1278, "timezone": "Europe/London"},
    "东京": {"latitude": 35.6762, "longitude": 139.6503, "timezone": "Asia/Tokyo"},
    "巴黎": {"latitude": 48.8566, "longitude": 2.3522, "timezone": "Europe/Paris"},
    "悉尼": {"latitude": -33.8688, "longitude": 151.2093, "timezone": "Australia/Sydney"},
    "新加坡": {"latitude": 1.3521, "longitude": 103.8198, "timezone": "Asia/Singapore"},
}

class WeatherServer:
    """天气查询 MCP 服务器"""
    
    def __init__(self):
        self.tools = [
            Tool(
                name="get_current_weather",
                title="获取当前天气",
                description="获取指定城市的当前天气状况",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，例如：北京、上海、杭州"
                        },
                        "language": {
                            "type": "string",
                            "description": "返回语言，可选值：zh（中文）、en（英文），默认为zh",
                            "enum": ["zh", "en"],
                            "default": "zh"
                        }
                    },
                    "required": ["city"]
                },
                outputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "temperature": {"type": "string"},
                        "weather": {"type": "string"},
                        "wind_direction": {"type": "string"},
                        "wind_speed": {"type": "string"},
                        "update_time": {"type": "string"},
                        "source": {"type": "string"}
                    }
                },
                icons=[],
                annotations={
                    "title": "获取当前天气工具",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": False
                },
                execution={
                    "taskSupport": "forbidden"
                }
            ),
            Tool(
                name="get_weather_forecast",
                title="获取天气预报",
                description="获取指定城市的天气预报（3天）",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，例如：北京、上海、杭州"
                        },
                        "days": {
                            "type": "integer",
                            "description": "预报天数，可选值：1-7，默认为3",
                            "minimum": 1,
                            "maximum": 7,
                            "default": 3
                        },
                        "language": {
                            "type": "string",
                            "description": "返回语言，可选值：zh（中文）、en（英文），默认为zh",
                            "enum": ["zh", "en"],
                            "default": "zh"
                        }
                    },
                    "required": ["city"]
                },
                outputSchema={
                    "type": "object",
                    "properties": {
                        "city": {"type": "string"},
                        "forecast_days": {"type": "integer"},
                        "forecasts": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "date": {"type": "string"},
                                    "weather": {"type": "string"},
                                    "max_temp": {"type": "string"},
                                    "min_temp": {"type": "string"},
                                    "precip": {"type": "string"}
                                }
                            }
                        },
                        "update_time": {"type": "string"},
                        "source": {"type": "string"}
                    }
                },
                icons=[],
                annotations={
                    "title": "获取天气预报工具",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": False
                },
                execution={
                    "taskSupport": "forbidden"
                }
            ),
            Tool(
                name="search_city",
                title="搜索城市",
                description="搜索城市，获取城市坐标信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "keyword": {
                            "type": "string",
                            "description": "搜索关键词，可以是城市名称、拼音或英文名"
                        },
                        "language": {
                            "type": "string",
                            "description": "返回语言，可选值：zh（中文）、en（英文），默认为zh",
                            "enum": ["zh", "en"],
                            "default": "zh"
                        }
                    },
                    "required": ["keyword"]
                },
                outputSchema={
                    "type": "object",
                    "properties": {
                        "search_keyword": {"type": "string"},
                        "total_results": {"type": "integer"},
                        "cities": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {"type": "string"},
                                    "latitude": {"type": "number"},
                                    "longitude": {"type": "number"},
                                    "timezone": {"type": "string"}
                                }
                            }
                        },
                        "note": {"type": "string"}
                    }
                },
                icons=[],
                annotations={
                    "title": "搜索城市工具",
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": False
                },
                execution={
                    "taskSupport": "forbidden"
                }
            )
        ]
        
        self.city_cache = {}  # 城市ID缓存
        self.http_client = httpx.AsyncClient(timeout=30.0)
        
    async def get_city_id(self, city_name: str, language: str = "zh") -> Optional[str]:
        """获取城市坐标信息（兼容性方法）"""
        # 现在直接返回城市名称，因为 open-meteo 使用坐标而不是城市ID
        return city_name
    
    async def get_current_weather(self, city: str, language: str = "zh") -> Dict[str, Any]:
        """获取当前天气（使用 open-meteo API）"""
        try:
            # 获取城市坐标
            city_info = self._get_city_coordinates(city)
            if not city_info:
                return {
                    "error": f"未找到城市 '{city}' 的坐标信息",
                    "suggestion": "请使用以下城市之一: " + ", ".join(sorted(CITY_COORDINATES.keys())[:10]) + " 等"
                }
            
            params = {
                "latitude": city_info["latitude"],
                "longitude": city_info["longitude"],
                "current_weather": "true",
                "timezone": city_info["timezone"],
                "forecast_days": 1
            }
            
            response = await self.http_client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            current = data["current_weather"]
            
            # 转换风向角度为方向
            wind_direction = self._degrees_to_direction(current["winddirection"])
            
            # 转换天气代码为描述
            weather_code = current.get("weathercode", 0)
            weather_desc = self._weathercode_to_description(weather_code, language)
            
            weather_info = {
                "city": city_info["name"],
                "temperature": f"{current['temperature']}°C",
                "weather": weather_desc,
                "wind_direction": wind_direction,
                "wind_speed": f"{current['windspeed']} km/h",
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "open-meteo"
            }
            
            return weather_info
                
        except httpx.HTTPError as e:
            return {"error": f"API请求失败: {str(e)}"}
        except Exception as e:
            return {"error": f"获取天气数据时出错: {str(e)}"}
    
    def _get_city_coordinates(self, city: str) -> Optional[Dict[str, Any]]:
        """获取城市坐标信息"""
        # 精确匹配
        if city in CITY_COORDINATES:
            return {"name": city, **CITY_COORDINATES[city]}
        
        # 模糊匹配（不区分大小写）
        city_lower = city.lower()
        for city_name, info in CITY_COORDINATES.items():
            if city_lower in city_name.lower() or city_name.lower() in city_lower:
                return {"name": city_name, **info}
        
        # 拼音匹配（简单实现）
        pinyin_map = {
            "beijing": "北京",
            "shanghai": "上海",
            "guangzhou": "广州",
            "shenzhen": "深圳",
            "hangzhou": "杭州",
            "chengdu": "成都",
            "chongqing": "重庆",
            "wuhan": "武汉",
            "xian": "西安",
            "nanjing": "南京"
        }
        
        if city_lower in pinyin_map:
            chinese_name = pinyin_map[city_lower]
            if chinese_name in CITY_COORDINATES:
                return {"name": chinese_name, **CITY_COORDINATES[chinese_name]}
        
        return None
    
    def _degrees_to_direction(self, degrees: float) -> str:
        """将角度转换为风向"""
        directions = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"]
        index = round(degrees / 45) % 8
        return directions[index]
    
    def _weathercode_to_description(self, code: int, language: str = "zh") -> str:
        """将天气代码转换为描述"""
        # WMO 天气代码映射
        weather_codes = {
            0: "晴",
            1: "基本晴朗",
            2: "部分多云",
            3: "阴天",
            45: "雾",
            48: "雾",
            51: "小雨",
            53: "中雨",
            55: "大雨",
            56: "冻雨",
            57: "冻雨",
            61: "小雨",
            63: "中雨",
            65: "大雨",
            66: "冻雨",
            67: "冻雨",
            71: "小雪",
            73: "中雪",
            75: "大雪",
            77: "雪粒",
            80: "阵雨",
            81: "强阵雨",
            82: "暴雨",
            85: "阵雪",
            86: "强阵雪",
            95: "雷暴",
            96: "雷暴伴有冰雹",
            99: "强雷暴伴有冰雹"
        }
        
        if language == "en":
            # 英文描述
            weather_codes = {
                0: "Clear sky",
                1: "Mainly clear",
                2: "Partly cloudy",
                3: "Overcast",
                45: "Fog",
                48: "Fog",
                51: "Light drizzle",
                53: "Moderate drizzle",
                55: "Dense drizzle",
                56: "Light freezing drizzle",
                57: "Dense freezing drizzle",
                61: "Slight rain",
                63: "Moderate rain",
                65: "Heavy rain",
                66: "Light freezing rain",
                67: "Heavy freezing rain",
                71: "Slight snow",
                73: "Moderate snow",
                75: "Heavy snow",
                77: "Snow grains",
                80: "Slight rain showers",
                81: "Moderate rain showers",
                82: "Violent rain showers",
                85: "Slight snow showers",
                86: "Heavy snow showers",
                95: "Thunderstorm",
                96: "Thunderstorm with slight hail",
                99: "Thunderstorm with heavy hail"
            }
        
        return weather_codes.get(code, "未知")
    
    async def get_weather_forecast(self, city: str, days: int = 3, language: str = "zh") -> Dict[str, Any]:
        """获取天气预报（使用 open-meteo API）"""
        try:
            # 获取城市坐标
            city_info = self._get_city_coordinates(city)
            if not city_info:
                return {
                    "error": f"未找到城市 '{city}' 的坐标信息",
                    "suggestion": "请使用以下城市之一: " + ", ".join(sorted(CITY_COORDINATES.keys())[:10]) + " 等"
                }
            
            # 限制天数在1-7之间
            days = max(1, min(days, 7))
            
            params = {
                "latitude": city_info["latitude"],
                "longitude": city_info["longitude"],
                "daily": "temperature_2m_max,temperature_2m_min,weathercode,precipitation_sum",
                "timezone": city_info["timezone"],
                "forecast_days": days
            }
            
            response = await self.http_client.get(OPEN_METEO_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            forecasts = []
            daily = data["daily"]
            
            for i in range(min(days, len(daily["time"]))):
                date = daily["time"][i]
                max_temp = daily["temperature_2m_max"][i]
                min_temp = daily["temperature_2m_min"][i]
                weather_code = daily["weathercode"][i]
                precip = daily["precipitation_sum"][i]
                
                weather_desc = self._weathercode_to_description(weather_code, language)
                
                forecast = {
                    "date": date,
                    "weather": weather_desc,
                    "max_temp": f"{max_temp}°C",
                    "min_temp": f"{min_temp}°C",
                    "precip": f"{precip} mm"
                }
                forecasts.append(forecast)
            
            return {
                "city": city_info["name"],
                "forecast_days": days,
                "forecasts": forecasts,
                "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "open-meteo"
            }
                
        except httpx.HTTPError as e:
            return {"error": f"API请求失败: {str(e)}"}
        except Exception as e:
            return {"error": f"获取天气预报时出错: {str(e)}"}
    
    async def search_city(self, keyword: str, language: str = "zh") -> Dict[str, Any]:
        """搜索城市（基于本地数据库）"""
        try:
            keyword_lower = keyword.lower().strip()
            matched_cities = []
            
            # 搜索匹配的城市
            for city_name, city_info in CITY_COORDINATES.items():
                # 检查是否匹配
                if (keyword_lower in city_name.lower() or 
                    city_name.lower() in keyword_lower or
                    self._match_pinyin(keyword_lower, city_name)):
                    
                    city_data = {
                        "name": city_name,
                        "latitude": city_info["latitude"],
                        "longitude": city_info["longitude"],
                        "timezone": city_info["timezone"]
                    }
                    matched_cities.append(city_data)
            
            # 按匹配度排序（完全匹配优先）
            matched_cities.sort(key=lambda x: 
                0 if x["name"].lower() == keyword_lower else
                1 if keyword_lower in x["name"].lower() else
                2)
            
            # 限制返回数量
            matched_cities = matched_cities[:10]
            
            if matched_cities:
                return {
                    "search_keyword": keyword,
                    "total_results": len(matched_cities),
                    "cities": matched_cities,
                    "note": "基于本地城市数据库搜索"
                }
            else:
                return {
                    "error": f"未找到匹配的城市: {keyword}",
                    "suggestion": "请尝试使用其他名称或查看支持的城市列表"
                }
                
        except Exception as e:
            return {"error": f"搜索城市时出错: {str(e)}"}
    
    def _match_pinyin(self, pinyin: str, chinese_name: str) -> bool:
        """简单拼音匹配（仅支持常见城市）"""
        pinyin_map = {
            "北京": "beijing",
            "上海": "shanghai",
            "广州": "guangzhou",
            "深圳": "shenzhen",
            "杭州": "hangzhou",
            "成都": "chengdu",
            "重庆": "chongqing",
            "武汉": "wuhan",
            "西安": "xian",
            "南京": "nanjing"
        }
        
        if chinese_name in pinyin_map:
            return pinyin in pinyin_map[chinese_name]
        return False
    
    async def handle_tool_call(self, tool_name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """处理工具调用"""
        try:
            if tool_name == "get_current_weather":
                city = arguments.get("city", "")
                language = arguments.get("language", "zh")
                result = await self.get_current_weather(city, language)
                
            elif tool_name == "get_weather_forecast":
                city = arguments.get("city", "")
                days = arguments.get("days", 3)
                language = arguments.get("language", "zh")
                result = await self.get_weather_forecast(city, days, language)
                
            elif tool_name == "search_city":
                keyword = arguments.get("keyword", "")
                language = arguments.get("language", "zh")
                result = await self.search_city(keyword, language)
                
            else:
                result = {"error": f"未知工具: {tool_name}"}
            
            # 将结果转换为文本内容
            content = self._format_result(tool_name, result)
            return CallToolResult(
                content=[TextContent(
                    type="text", 
                    text=content, 
                    annotations={
                        "audience": ["user"],
                        "priority": 0.5
                    }
                )],
                structuredContent={},
                isError="error" in result
            )
            
        except Exception as e:
            error_content = f"处理工具调用时出错: {str(e)}"
            return CallToolResult(
                content=[TextContent(
                    type="text", 
                    text=error_content, 
                    annotations={
                        "audience": ["user"],
                        "priority": 1.0
                    }
                )],
                structuredContent={},
                isError=True
            )
    
    def _format_result(self, tool_name: str, result: Dict[str, Any]) -> str:
        """格式化结果为文本"""
        if "error" in result:
            error_msg = f"错误: {result['error']}"
            if "suggestion" in result:
                error_msg += f"\n建议: {result['suggestion']}"
            return error_msg
        
        if tool_name == "get_current_weather":
            weather_text = f"""🌤️ {result['city']} 当前天气
温度: {result['temperature']}"""
            
            if 'feels_like' in result:
                weather_text += f" (体感 {result['feels_like']})"
            
            weather_text += f"""
天气: {result['weather']}
风向: {result['wind_direction']} {result['wind_speed']}"""
            
            if 'wind_speed_kmh' in result:
                weather_text += f" ({result['wind_speed_kmh']})"
            
            if 'humidity' in result:
                weather_text += f"""
湿度: {result['humidity']}"""
            
            if 'pressure' in result:
                weather_text += f"""
气压: {result['pressure']}"""
            
            if 'visibility' in result:
                weather_text += f"""
能见度: {result['visibility']}"""
            
            if 'cloud_cover' in result:
                weather_text += f"""
云量: {result['cloud_cover']}"""
            
            weather_text += f"""
更新时间: {result['update_time']}
数据来源: {result.get('source', '未知')}"""
            
            if 'note' in result:
                weather_text += f"\n备注: {result['note']}"
            
            return weather_text
        
        elif tool_name == "get_weather_forecast":
            forecast_text = f"🌤️ {result['city']} {result['forecast_days']}天天气预报\n\n"
            for i, forecast in enumerate(result['forecasts']):
                forecast_text += f"📅 {forecast['date']}:\n"
                forecast_text += f"  天气: {forecast['weather']}\n"
                forecast_text += f"  温度: {forecast['min_temp']} ~ {forecast['max_temp']}\n"
                if forecast.get('precip', '0 mm') != '0 mm':
                    forecast_text += f"  降水: {forecast['precip']}\n"
                forecast_text += "\n"
            
            if result.get('update_time'):
                forecast_text += f"更新时间: {result['update_time']}"
            return forecast_text
        
        elif tool_name == "search_city":
            cities_text = f"🔍 搜索 '{result['search_keyword']}' 找到 {result['total_results']} 个结果:\n\n"
            for i, city in enumerate(result['cities'], 1):
                cities_text += f"{i}. {city['name']}\n"
                cities_text += f"   坐标: {city['latitude']}, {city['longitude']}\n"
                if city.get('timezone'):
                    cities_text += f"   时区: {city['timezone']}\n"
                cities_text += "\n"
            return cities_text
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    async def close(self):
        """关闭资源"""
        await self.http_client.aclose()


async def main():
    """主函数 - 简单的 MCP 服务器实现"""
    server = WeatherServer()
    
    # 简单的 MCP 服务器循环
    import json
    
    try:
        # 读取 stdin，写入 stdout
        while True:
            try:
                # 读取一行 JSON-RPC 消息
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                # 解析消息
                try:
                    message = json.loads(line)
                except json.JSONDecodeError:
                    print(f"无法解析 JSON: {line}", file=sys.stderr)
                    continue
                
                method = message.get("method")
                message_id = message.get("id")
                
                if method == "initialize":
                    # MCP 初始化请求
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {}
                            },
                            "serverInfo": {
                                "name": "weather-mcp-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                elif method == "tools/list":
                    # 返回工具列表
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": {
                            "tools": [tool.model_dump() for tool in server.tools]
                        }
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                elif method == "tools/call":
                    # 处理工具调用
                    params = message.get("params", {})
                    tool_name = params.get("name")
                    arguments = params.get("arguments", {})
                    
                    result = await server.handle_tool_call(tool_name, arguments)
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": result.model_dump()
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                elif method == "ping":
                    # 响应 ping
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "result": "pong"
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                elif method == "notifications/initialized":
                    # 初始化完成通知，无需响应
                    pass
                    
                else:
                    # 未知方法
                    response = {
                        "jsonrpc": "2.0",
                        "id": message_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
            except Exception as e:
                print(f"处理消息时出错: {e}", file=sys.stderr)
                
    except KeyboardInterrupt:
        print("服务器收到中断信号", file=sys.stderr)
    except Exception as e:
        print(f"服务器运行出错: {e}", file=sys.stderr)
    finally:
        await server.close()


if __name__ == "__main__":
    # 检查是否以 stdio 模式运行
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        # stdio 模式 - 由 MCP 客户端调用
        print("MCP 天气服务器启动（使用 open-meteo API）", file=sys.stderr)
        print(f"支持 {len(CITY_COORDINATES)} 个城市", file=sys.stderr)
        asyncio.run(main())
    else:
        # 独立运行模式 - 显示帮助信息
        print("MCP 天气服务器（open-meteo 版本）")
        print("=" * 50)
        print()
        print("这个文件应该作为 MCP 服务器运行，而不是直接执行。")
        print()
        print("特点:")
        print("✅ 无需 API 密钥")
        print(f"✅ 支持 {len(CITY_COORDINATES)} 个城市")
        print("✅ 包含中国主要城市和国际城市")
        print("✅ 提供当前天气和天气预报")
        print()
        print("使用方法:")
        print("1. 作为 MCP 服务器运行:")
        print("   python weather_server.py --stdio")
        print()
        print("2. 使用 server.py 启动完整服务器:")
        print("   python server.py")
        print()
        print("3. 运行测试:")
        print("   python test_client.py")
        print()
        print("4. 查看支持的城市:")
        print("   python -c \"from weather_server import CITY_COORDINATES; print('支持的城市:', ', '.join(sorted(CITY_COORDINATES.keys())))\"")
        print()
        sys.exit(0)
