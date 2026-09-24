import asyncio

from session_collection.session_manager import (
    session_manager,
)


async def main():

    session_id = "test-session-001"

    # ==============================
    # 本地工具
    # ==============================

    selected_tools = [
        "attendance",
        "weather",
    ]

    # ==============================
    # MCP
    # ==============================

    selected_mcps = [
        "amap_maps", "cook_maps"
    ]

    # ==============================
    # 第一轮
    # ==============================

    response1 = await session_manager.chat(

        session_id=session_id,

        message=(
            "我想从南京市江宁区淳化街道的武夷绿洲品兰苑小区出发骑行到江苏省南京市江宁区秣陵街道清水亭东路 1266 号，"
            "请你给出骑行规划"
        ),

        selected_tools=selected_tools,

        selected_mcps=selected_mcps,
    )

    print("\n第一轮 Agent：")
    print(response1)

    # ==============================
    # 第二轮
    # ==============================

    response2 = await session_manager.chat(

        session_id=session_id,

        message="给出小龙虾的做法，包括食材和步骤",

        selected_tools=selected_tools,

        selected_mcps=selected_mcps,
    )

    print("\n第二轮 Agent：")
    print(response2)


    # ==============================
    # 第三轮
    # ==============================

    response3 = await session_manager.chat(

        session_id=session_id,

        message="我想要查询这个月大数据部门的考勤情况",

        selected_tools=selected_tools,

        selected_mcps=selected_mcps,
    )

    print("\n第二轮 Agent：")
    print(response3)

if __name__ == "__main__":
    asyncio.run(main())