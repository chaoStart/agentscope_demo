from importlib import import_module
from typing import Any


# ==========================================
# Tool 注册表
# ==========================================
#
# 注意：
# 这里只保存字符串。
#
# 不要：
# from tools_collection.weather import weather_tool
#
# 否则 weather.py 在启动阶段就已经被加载。
# ==========================================

TOOL_REGISTRY = {

    "weather": {
        "name": "天气查询",
        "description": "查询城市当前实时天气",
        "module": "tools_collection.weather",
        "attribute": "weather_tool",
    },

    "attendance": {
        "name": "公司考勤查询",
        "description": "查询公司部门的月、周、日考勤情况",
        "module": "tools_collection.company",
        "attribute": "attendance_tool",
    },
}


def load_tool(tool_name: str) -> Any:
    """动态加载单个 Tool。"""

    config = TOOL_REGISTRY.get(tool_name)

    if config is None:
        raise ValueError(
            f"不存在工具：{tool_name}，"
            f"可用工具：{list(TOOL_REGISTRY.keys())}"
        )

    module_name = config["module"]
    attribute_name = config["attribute"]

    print(
        f"[ToolLoader] 正在加载工具："
        f"{tool_name} -> {module_name}"
    )

    # 真正到这里才 import 对应 Python 文件
    module = import_module(module_name)

    tool = getattr(
        module,
        attribute_name,
    )

    return tool


def load_tools(
    tool_names: list[str] | None,
) -> list[Any]:
    """根据前端选择动态加载多个 Tool。

    Args:
        tool_names:
            前端选择的工具名称。

            例如：
            ["attendance"]

            或：
            ["attendance", "weather"]

    Returns:
        AgentScope Tool 列表。
    """

    if not tool_names:
        return []

    tools = []

    # 去重，保持原始顺序
    unique_names = list(
        dict.fromkeys(tool_names)
    )

    for tool_name in unique_names:
        tool = load_tool(tool_name)

        tools.append(tool)

    print(
        "[ToolLoader] 最终加载工具：",
        unique_names,
    )

    return tools


def get_available_tools() -> list[dict]:
    """返回可供前端展示的工具列表。

    此函数不会 import 实际 Tool 模块。
    """

    result = []

    for tool_id, config in TOOL_REGISTRY.items():

        result.append(
            {
                "id": tool_id,
                "name": config["name"],
                "description": config["description"],
            }
        )

    return result