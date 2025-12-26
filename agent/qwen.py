from openai import OpenAI
from datetime import datetime
import json
import os

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    # 新加坡和北京地域的API Key不同。获取API Key：https://help.aliyun.com/zh/model-studio/get-api-key
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    # 以下是北京地域base_url，如果使用新加坡地域的模型，需要将base_url替换为：https://dashscope-intl.aliyuncs.com/compatible-mode/v1
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",  # 填写DashScope SDK的base_url
)

# 定义工具列表，模型在选择使用哪个工具时会参考工具的name和description
tools = [
    # 工具1 获取当前时刻的时间
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            # 因为获取当前时间无需输入参数，因此parameters为空字典
            "parameters": {}
        }
    },
    # 工具2 获取指定城市的天气
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": { 
                "type": "object",
                "properties": {
                    # 查询天气时需要提供位置，因此参数设置为location
                    "location": {
                        "type": "string",
                        "description": "城市或县区，比如北京市、杭州市、余杭区等。"
                    }
                }
            },
            "required": [
                "location"
            ]
        }
    }
]

# 模拟天气查询工具。返回结果示例：“北京今天是雨天。”
def get_current_weather(location):
    return f"{location}今天是雨天。 "

# 查询当前时间的工具。返回结果示例：“当前时间：2024-04-15 17:15:18。“
def get_current_time():
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 格式化当前日期和时间
    formatted_time = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    # 返回格式化后的当前时间
    return f"当前时间：{formatted_time}。"

# 封装模型响应函数
def get_response(messages):
    completion = client.chat.completions.create(
        model="qwen-plus",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=messages,
        tools=tools
        )
    return completion.model_dump()

def call_with_messages():
    print('\n')
    messages = [
            {
                "content": input('请输入：'),  # 提问示例："现在几点了？" "一个小时后几点" "北京天气如何？"
                "role": "user"
            }
    ]
    print("-"*60)
    # 模型的第一轮调用
    i = 1
    first_response = get_response(messages)
    assistant_output = first_response['choices'][0]['message']
    print(f"\n第{i}轮大模型输出信息：{first_response}\n")
    if  assistant_output['content'] is None:
        assistant_output['content'] = ""
    messages.append(assistant_output)
    # 如果不需要调用工具，则直接返回最终答案
    if assistant_output['tool_calls'] == None:  # 如果模型判断无需调用工具，则将assistant的回复直接打印出来，无需进行模型的第二轮调用
        print(f"无需调用工具，我可以直接回复：{assistant_output['content']}")
        return
    # 如果需要调用工具，则进行模型的多轮调用，直到模型判断无需调用工具
    while assistant_output['tool_calls'] != None:
        # 如果判断需要调用查询天气工具，则运行查询天气工具
        if assistant_output['tool_calls'][0]['function']['name'] == 'get_current_weather':
            tool_info = {"name": "get_current_weather", "role":"tool"}
            # 提取位置参数信息
            location = json.loads(assistant_output['tool_calls'][0]['function']['arguments'])['location']
            tool_info['content'] = get_current_weather(location)
        # 如果判断需要调用查询时间工具，则运行查询时间工具
        elif assistant_output['tool_calls'][0]['function']['name'] == 'get_current_time':
            tool_info = {"name": "get_current_time", "role":"tool"}
            tool_info['content'] = get_current_time()
        print(f"工具输出信息：{tool_info['content']}\n")
        print("-"*60)
        messages.append(tool_info)
        assistant_output = get_response(messages)['choices'][0]['message']
        if  assistant_output['content'] is None:
            assistant_output['content'] = ""
        messages.append(assistant_output)
        i += 1
        print(f"第{i}轮大模型输出信息：{assistant_output}\n")
    print(f"最终答案：{assistant_output['content']}")

if __name__ == '__main__':
    call_with_messages()