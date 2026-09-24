# mcp_collection/amap_mcp.py

import os

from agentscope.mcp import (
    MCPClient,
    HttpMCPConfig,
)


# 建议实际项目把 URL 放进 .env
MODELSCOPE_COOK_MCP_URL = os.getenv("MODELSCOPE_COOK_MCP_URL", "https://mcp.api-inference.modelscope.net/4617ba1669d74c/mcp")

cook_mcp_client = MCPClient(
    name="cook_maps",

    # SSE 属于远程 HTTP MCP。
    # 这里使用长连接模式，应用启动时 connect，
    # 应用结束时 close。
    # is_stateful=True,
    is_stateful=False,

    mcp_config=HttpMCPConfig(
        url=MODELSCOPE_COOK_MCP_URL,
        timeout=30.0,
    ),

    # None = 暴露该 MCP Server 提供的全部工具
    enable_tools=None,

    # 不主动禁用工具
    disable_tools=None,

    # MCP 工具实际执行超时时间
    execution_timeout=60.0,
)