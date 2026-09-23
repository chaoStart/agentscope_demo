import asyncio
from dataclasses import dataclass

from agentscope.agent import Agent
from agentscope.message import UserMsg

from agent_collection.agent_factory import (
    create_agent,
)


@dataclass
class SessionEntry:
    agent: Agent
    selected_tools: tuple[str, ...]
    lock: asyncio.Lock


class SessionManager:
    """管理多个用户会话。"""

    def __init__(self):
        self._sessions: dict[
            str,
            SessionEntry
        ] = {}

    def _normalize_tools(
        self,
        selected_tools: list[str],
    ) -> tuple[str, ...]:

        return tuple(
            sorted(set(selected_tools))
        )

    def get_or_create_session(
        self,
        session_id: str,
        selected_tools: list[str],
    ) -> SessionEntry:

        tool_signature = self._normalize_tools(
            selected_tools
        )

        entry = self._sessions.get(
            session_id
        )

        # ==============================
        # 第一次进入当前会话
        # ==============================

        if entry is None:

            agent = create_agent(
                selected_tools=list(
                    tool_signature
                )
            )

            entry = SessionEntry(
                agent=agent,
                selected_tools=tool_signature,
                lock=asyncio.Lock(),
            )

            self._sessions[
                session_id
            ] = entry

            print(
                f"[Session] 创建新会话："
                f"{session_id}"
            )

            return entry

        # ==============================
        # 用户修改了前端选择的工具
        # ==============================

        if (
            entry.selected_tools
            != tool_signature
        ):

            print(
                f"[Session] 工具发生变化："
                f"{entry.selected_tools}"
                f" -> {tool_signature}"
            )

            # 保存原来的上下文状态
            old_state = entry.agent.state

            # 使用新 Toolkit 创建 Agent，
            # 但继续使用原来的 AgentState
            new_agent = create_agent(
                selected_tools=list(
                    tool_signature
                ),
                state=old_state,
            )

            entry.agent = new_agent
            entry.selected_tools = (
                tool_signature
            )

        return entry

    async def chat(
        self,
        session_id: str,
        message: str,
        selected_tools: list[str],
    ) -> str:

        entry = self.get_or_create_session(
            session_id=session_id,
            selected_tools=selected_tools,
        )

        # 同一 session 不允许同时处理两条消息，
        # 避免上下文顺序错乱
        async with entry.lock:

            msg = UserMsg(
                name="user",
                content=message,
            )

            result = await entry.agent.reply(
                msg
            )

            return result.get_text_content()


session_manager = SessionManager()