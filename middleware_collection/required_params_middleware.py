# middleware_collection/required_params_middleware.py

from typing import Any, AsyncGenerator, Callable

from agentscope.tool import (
    ToolMiddlewareBase,
    ToolChunk,
)

from toolkit_collection.tool_validator import (
    get_missing_required_params,
)


class RequiredParamsMiddleware(ToolMiddlewareBase):
    """Tool必填参数统一校验中间件。"""

    async def on_tool_call(
        self,
        tool,
        input_kwargs: dict[str, Any],
        next_handler: Callable[..., AsyncGenerator[ToolChunk, None]],
    ) -> AsyncGenerator[
        ToolChunk,
        None
    ]:

        print(
            f"[ToolValidator] 检查工具："
            f"{tool.name}"
        )

        print(
            f"[ToolValidator] 参数："
            f"{input_kwargs}"
        )

        # ==========================
        # 1. 检查缺失必填参数
        # ==========================

        missing_params = (
            get_missing_required_params(
                input_schema=tool.input_schema,
                tool_args=input_kwargs,
            )
        )

        # ==========================
        # 2. 参数缺失
        # ==========================

        if missing_params:

            print(
                f"[ToolValidator] "
                f"缺少参数：{missing_params}"
            )

            # 不调用 next_handler
            # = 不执行真实 Tool

            message = (
                f"工具 {tool.name} "
                f"暂时无法执行，"
                f"缺少以下必填参数："
                f"{', '.join(missing_params)}。"
                f"请向用户询问缺失信息，"
                f"获取后再继续执行原任务。"
            )

            yield ToolChunk(
                content=message
            )

            return

        # ==========================
        # 3. 参数完整
        # ==========================

        print(
            "[ToolValidator] 参数完整，"
            "继续执行工具。"
        )

        async for chunk in next_handler(
            **input_kwargs
        ):
            yield chunk