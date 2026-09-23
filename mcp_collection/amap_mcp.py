# mcp_collection/amap_mcp.py

import os

from agentscope.mcp import (
    MCPClient,
    HttpMCPConfig,
)


# 建议实际项目把 URL 放进 .env
MODELSCOPE_AMAP_MCP_URL = os.getenv("MODELSCOPE_AMAP_MCP_URL", "https://mcp.api-inference.modelscope.net/6828c475302149/sse", )

amap_mcp_client = MCPClient(
    name="amap_maps",

    # SSE 属于远程 HTTP MCP。
    # 这里使用长连接模式，应用启动时 connect，
    # 应用结束时 close。
    is_stateful=True,

    mcp_config=HttpMCPConfig(
        url=MODELSCOPE_AMAP_MCP_URL,
        timeout=30.0,
    ),

    # None = 暴露该 MCP Server 提供的全部工具
    enable_tools=None,

    # 不主动禁用工具
    disable_tools=None,

    # MCP 工具实际执行超时时间
    execution_timeout=60.0,
)


async def connect_amap_mcp() -> None:
    """连接魔搭高德地图 MCP 服务。"""

    if amap_mcp_client.is_connected:
        print("[MCP] amap_maps 已连接")
        return

    print(
        "[MCP] 正在连接高德地图 MCP：",
        MODELSCOPE_AMAP_MCP_URL,
    )

    await amap_mcp_client.connect()

    print("[MCP] amap_maps 连接成功")


async def print_amap_tools() -> None:
    """打印高德 MCP 暴露的全部工具，用于开发调试。"""

    tools = await amap_mcp_client.list_tools()

    print(
        f"[MCP] amap_maps 共发现 {len(tools)} 个工具："
    )

    for index, tool in enumerate(tools, start=1):
        print(
            f"{index}. "
            f"name={tool.name}"
        )
        print(f"   is_read_only= {tool.is_read_only}")
        print(
            f"   description="
            f"{tool.description}"
        )


async def close_amap_mcp() -> None:
    """关闭高德地图 MCP 长连接。"""

    if not amap_mcp_client.is_connected:
        return

    await amap_mcp_client.close()

    print("[MCP] amap_maps 已关闭")