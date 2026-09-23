import os

from agentscope.agent import Agent
from agentscope.model import DashScopeChatModel
from agentscope.credential import DashScopeCredential
from agentscope.state import AgentState

from toolkit_collection.toolkit_factory import (create_toolkit,)
from dotenv import load_dotenv
# 加载环境变量，必须放在前面
load_dotenv()

SYSTEM_PROMPT = """
你是企业智能助手。

你可以根据当前 Toolkit 中实际提供的工具，
自主选择合适能力完成用户任务。

调用工具前必须检查所有必填参数。

如果已经明确知道用户想使用某项能力，
但是缺少必要参数：

1. 不允许猜测；
2. 不要调用工具；
3. 向用户询问缺失的信息；
4. 等用户下一轮补充；
5. 结合之前的对话上下文继续原任务。

用户下一轮可能只回复一个很短的信息，
例如：

“攀枝花”

你必须结合前面的对话判断，
它是否是在补充之前缺失的参数。

参数完整之后，再调用相应工具。

对于实时或企业内部数据，
必须优先使用工具获取结果，不允许自行编造。

调用任何 Tool、Skill 或 MCP Tool 前，
检查其必填参数。

如果必填参数缺失：

1. 如果缺失参数可以通过当前已有 Tool/MCP 自动获得，
   优先调用相应工具获取，不要询问用户。

2. 如果缺失参数只能由用户提供，
   不允许猜测，应向用户询问。

3. 用户下一轮补充后，
   必须结合当前会话上下文继续之前未完成的任务。

4. 不要因为缺少一个参数就放弃原任务。
"""


def create_agent(
    selected_tools: list[str],
    state: AgentState | None = None,
) -> Agent:
    """创建企业智能体。"""

    toolkit = create_toolkit(
        selected_tools=selected_tools,
        enable_skills=True,

        # 这里根据实际情况控制
        enable_amap_mcp=False,
    )

    agent = Agent(
        name="enterprise_agent",

        system_prompt=SYSTEM_PROMPT,

        model=DashScopeChatModel(
            credential=DashScopeCredential(
                api_key=os.environ[
                    "DASHSCOPE_API_KEY"
                ]
            ),

            model="qwen-max",

            stream=True,
        ),

        toolkit=toolkit,

        # 非常重要：
        # 可以把已有 AgentState 交给新 Agent
        state=state,
    )

    return agent