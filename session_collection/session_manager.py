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
    selected_mcps: tuple[str, ...]
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

    async def get_or_create_session(
            self,
            session_id: str,
            selected_tools: list[str],
            selected_mcps: list[str] | None = None,
    ) -> SessionEntry:

        tool_signature = tuple(
            sorted(
                set(selected_tools or [])
            )
        )

        mcp_signature = tuple(
            sorted(
                set(selected_mcps or [])
            )
        )

        entry = self._sessions.get(
            session_id
        )

        # ==============================
        # 新会话
        # ==============================

        if entry is None:
            agent = await create_agent(
                selected_tools=list(
                    tool_signature
                ),

                selected_mcps=list(
                    mcp_signature
                ),
            )

            entry = SessionEntry(
                agent=agent,

                selected_tools=(
                    tool_signature
                ),

                selected_mcps=(
                    mcp_signature
                ),

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
        # Tool 或 MCP 配置发生变化
        # ==============================

        if (
                entry.selected_tools
                != tool_signature
                or
                entry.selected_mcps
                != mcp_signature
        ):
            old_state = (
                entry.agent.state
            )

            new_agent = await create_agent(
                selected_tools=list(
                    tool_signature
                ),

                selected_mcps=list(
                    mcp_signature
                ),

                # 保留会话上下文
                state=old_state,
            )

            entry.agent = new_agent

            entry.selected_tools = (
                tool_signature
            )

            entry.selected_mcps = (
                mcp_signature
            )

        return entry

    async def chat(
        self,
        session_id: str,
        message: str,
        selected_tools: list[str],
        selected_mcps: list[str] | None = None,
    ) -> str:

        entry = await self.get_or_create_session(
            session_id=session_id,

            selected_tools=selected_tools,

            selected_mcps=selected_mcps,
        )

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