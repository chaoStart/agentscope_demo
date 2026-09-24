from agentscope.tool import Toolkit

from tools_collection.tool_loader import (
    load_tools,
)

from skills_collection.skill_loader import (
    skill_loader,
)

from mcp_collection.mcp_loader import (
    load_mcps,
)


async def create_toolkit(
        selected_tools: list[str] | None = None,
        selected_mcps: list[str] | None = None,
        enable_skills: bool = True,
) -> Toolkit:
    # ==========================
    # 1. 动态加载本地 Tool
    # ==========================

    tools = load_tools(
        selected_tools
    )

    # ==========================
    # 2. 动态加载 MCP
    # ==========================

    mcps = await load_mcps(
        selected_mcps
    )

    # ==========================
    # 3. Skill
    # ==========================

    skill_loaders = (
        [skill_loader]
        if enable_skills
        else []
    )

    # ==========================
    # 4. 创建统一 Toolkit
    # ==========================

    toolkit = Toolkit(
        tools=tools,
        skills_or_loaders=skill_loaders,
        mcps=mcps,
    )

    return toolkit
