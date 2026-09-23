import asyncio

from session_collection.session_manager import (
    session_manager,
)


async def main():

    session_id = "test-session-001"

    selected_tools = [
        "attendance",
        "weather",
    ]

    # ==================================
    # 第一轮
    # ==================================

    response1 = await session_manager.chat(
        session_id=session_id,

        message="今天的天气怎么样？",

        selected_tools=selected_tools,
    )

    print("\n第一轮 Agent：")
    print(response1)

    # ==================================
    # 模拟 Human-in-the-loop
    #
    # 实际项目中这里不是写死，
    # 而是前端用户下一次输入
    # ==================================

    response2 = await session_manager.chat(
        session_id=session_id,

        message="攀枝花",

        selected_tools=selected_tools,
    )

    print("\n第二轮 Agent：")
    print(response2)


if __name__ == "__main__":
    asyncio.run(main())