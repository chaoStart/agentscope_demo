import os

from agentscope.agent import Agent
from agentscope.model import DashScopeChatModel
from agentscope.credential import DashScopeCredential
from agentscope.permission import PermissionMode

from toolkit_collection.toolkit_factory import (
    create_toolkit,
)


SYSTEM_PROMPT = """
你是企业智能助手。

你只能使用当前 Toolkit 中实际加载的 Tool、Skill 和 MCP。

调用工具时遵循以下原则：

1. 根据用户问题选择合适工具。

2. 如果需要调用工具，但缺少只能由用户提供的必要参数：
   - 不允许猜测；
   - 不要调用不相关的工具；
   - 向用户询问缺失参数。

3. 用户下一轮补充信息后，
   必须结合当前会话上下文继续之前未完成的任务。

4. 如果缺失的信息可以通过其他工具获得，
   应优先调用工具获得，而不是询问用户。

例如地图路线规划：
- 用户给了地点名称，但路线工具需要经纬度，
  可以先使用高德 maps_geo 得到经纬度；
- 用户没有提供起点，则应该询问用户起点。

5. 不允许因为某个工具暂时缺参，
   就擅自改用其他无关工具完成任务。

例如：
用户要骑行路线，但缺少起点时，
不能改为查询天气，
应该询问用户从哪里出发。
"""


async def create_agent(
    selected_tools: list[str],
    selected_mcps: list[str] | None = None,
    state=None,
):

    toolkit = await create_toolkit(
        selected_tools=selected_tools,
        selected_mcps=selected_mcps,
        enable_skills=True,
    )

    agent = Agent(
        name="enterprise_agent",
        system_prompt=SYSTEM_PROMPT,
        model=DashScopeChatModel(
            credential=DashScopeCredential(
                api_key=os.environ[
                    "DASHSCOPE_API_KEY"
                ],
            ),
            model="qwen-max",
            stream=True,
        ),

        toolkit=toolkit,

        state=state,
    )

    # Demo阶段，如果高德MCP仍触发权限确认
    agent.state.permission_context.mode = (
        PermissionMode.BYPASS
    )

    return agent