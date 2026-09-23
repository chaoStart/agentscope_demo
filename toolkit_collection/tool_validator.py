# toolkit_collection/tool_validator.py

from typing import Any


def get_missing_required_params(
    input_schema: dict[str, Any],
    tool_args: dict[str, Any],
) -> list[str]:
    """检查 Tool 调用是否缺少必填参数。"""

    required_fields = input_schema.get(
        "required",
        [],
    )

    missing_fields = []

    for field in required_fields:

        value = tool_args.get(field)

        if value is None:
            missing_fields.append(field)

        elif isinstance(value, str) and not value.strip():
            missing_fields.append(field)

    return missing_fields