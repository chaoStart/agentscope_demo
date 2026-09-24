from mcp_collection.amap_mcp import amap_mcp_client
from mcp_collection.howtocook_mcp import cook_mcp_client


MCP_REGISTRY = {

    "amap_maps": {
        "name": "高德地图",
        "description": "提供地理编码、POI搜索、骑行、驾车、步行、公交等地图能力",
        "client": amap_mcp_client,
    },
    "cook_maps": {
        "name": "烹饪大全",
        "description": "提供烹饪技巧、推荐饭菜、菜谱能力",
        "client": cook_mcp_client,
    },
}


async def load_mcps(
    mcp_names: list[str] | None,
):
    """动态加载前端选中的 MCP 服务。"""

    if not mcp_names:
        return []

    clients = []

    unique_names = list(dict.fromkeys(mcp_names))

    for mcp_name in unique_names:

        config = MCP_REGISTRY.get(mcp_name)

        if config is None:
            raise ValueError(
                f"不存在 MCP：{mcp_name}，"
                f"当前可用 MCP："
                f"{list(MCP_REGISTRY.keys())}"
            )

        client = config["client"]

        print(
            f"[MCPLoader] 正在加载 MCP："
            f"{mcp_name}"
        )

        # Stateful MCP 必须提前连接
        if client.is_stateful and not client.is_connected:

            print(
                f"[MCPLoader] 正在连接 MCP："
                f"{mcp_name}"
            )

            await client.connect()

            print(
                f"[MCPLoader] MCP连接成功："
                f"{mcp_name}"
            )

        clients.append(client)

    print("[MCPLoader] 最终加载 MCP：", unique_names,)

    return clients