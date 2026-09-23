from agentscope.tool import Toolkit

from tools_collection.tool_loader import (load_tools, )

from skills_collection.skill_loader import (skill_loader, )

from mcp_collection.amap_mcp import (amap_mcp_client, )


def create_toolkit(
    selected_tools: list[str] | None = None,
    enable_skills: bool = True,
    enable_amap_mcp: bool = True,
) -> Toolkit:
    """根据前端配置动态创建 Toolkit。

    Args:
        selected_tools:
            用户在前端选择的本地工具。

            例如：
            ["attendance"]

            或：
            ["weather", "attendance"]

        enable_skills:
            是否加载 Skills。

        enable_amap_mcp:
            是否加载高德 MCP。
    """

    # ==========================
    # 1. 动态加载本地 Tool
    # ==========================

    tools = load_tools(
        selected_tools
    )

    # ==========================
    # 2. 动态决定 Skill
    # ==========================

    skill_loaders = (
        [skill_loader]
        if enable_skills
        else []
    )

    # ==========================
    # 3. 动态决定 MCP
    # ==========================

    mcps = (
        [amap_mcp_client]
        if enable_amap_mcp
        else []
    )

    # ==========================
    # 4. 统一创建 Toolkit
    # ==========================

    toolkit = Toolkit(
        tools=tools,
        skills_or_loaders=skill_loaders,
        mcps=mcps,
    )

    return toolkit