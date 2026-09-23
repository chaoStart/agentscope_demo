import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from agentscope.tool import FunctionTool, Toolkit
from agentscope.permission import (
    PermissionDecision,
    PermissionBehavior,
)
from middleware_collection.required_params_middleware import (
    RequiredParamsMiddleware,
)


# =========================
# 1. 加载环境变量
# =========================

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


# =========================
# 2. 心知天气 API
# =========================

SENIVERSE_API_URL = (
    "https://api.seniverse.com/v3/weather/now.json"
)


# =========================
# 3. 天气查询工具
# =========================

def get_weather(
    location: str,
    unit: str = "c",
) -> str:
    """查询指定城市当前实时天气。

    Args:
        location:
            必填。需要查询的城市名称，例如南京、北京、攀枝花。
            城市名称必须来自用户明确提供的信息。
            如果当前对话中用户没有提供城市名称，
            不允许猜测城市，应先向用户询问具体城市。

        unit:
            温度单位。
            c 表示摄氏度，
            f 表示华氏度，
            默认 c。

    Returns:
        指定城市当前实时天气。
    """
    print(
        f"[get_weather] location={location}, unit={unit}"
    )

    api_key = os.getenv("SENIVERSE_API_KEY")

    if not api_key:
        return "天气查询失败：未配置 SENIVERSE_API_KEY。"

    params = {
        "key": api_key,
        "location": location,
        "language": "zh-Hans",
        "unit": unit,
    }

    try:
        response = requests.get(
            SENIVERSE_API_URL,
            params=params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            return f"未查询到 {location} 的天气信息。"

        result = results[0]

        city = result["location"]["name"]
        weather = result["now"]["text"]
        temperature = result["now"]["temperature"]
        last_update = result["last_update"]

        temperature_unit = (
            "℃"
            if unit == "c"
            else "℉"
        )

        return (
            f"城市：{city}\n"
            f"天气：{weather}\n"
            f"温度：{temperature}{temperature_unit}\n"
            f"更新时间：{last_update}"
        )

    except requests.Timeout:
        return f"查询 {location} 天气失败：请求超时。"

    except requests.RequestException as e:
        return (
            f"查询 {location} 天气失败："
            f"{str(e)}"
        )

    except (
        KeyError,
        IndexError,
        ValueError,
        TypeError,
    ) as e:
        return (
            f"天气数据解析失败：{str(e)}"
        )


# =========================
# 4. 注册 Tool
# =========================

weather_tool = FunctionTool(
    get_weather,
    middlewares=[
        RequiredParamsMiddleware(),
    ],
    permission=PermissionDecision(
        behavior=PermissionBehavior.ALLOW,
        message="天气查询属于只读操作，允许自动执行。",
    ),
)
