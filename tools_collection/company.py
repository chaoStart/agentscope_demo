from agentscope.tool import FunctionTool

from agentscope.permission import (
    PermissionDecision,
    PermissionBehavior,
)
from middleware_collection.required_params_middleware import (
    RequiredParamsMiddleware,
)


ATTENDANCE_DATA = {
    "大数据部门": {
        "月考勤": "缺席10人次",
        "周考勤": "缺席5人次",
        "日考勤": "缺席0次",
    }
}


def lookup_department(
    department_name: str,
    attendance_type: str,
) -> str:
    """查询公司指定部门的考勤情况。

    Args:
        department_name:
            部门名称，例如：研发部门。
        attendance_type:
            考勤统计类型，可选：
            月考勤、周考勤、日考勤。

    Returns:
        指定部门对应周期的考勤结果。
    """

    print(
        f"[lookup_department] "
        f"department_name={department_name}, "
        f"attendance_type={attendance_type}"
    )

    department_data = ATTENDANCE_DATA.get(
        department_name
    )

    if department_data is None:
        return (
            f"未查询到部门：{department_name}。"
            f"当前可查询部门："
            f"{'、'.join(ATTENDANCE_DATA.keys())}"
        )

    result = department_data.get(
        attendance_type
    )

    if result is None:
        return (
            f"不支持考勤类型：{attendance_type}。"
            "当前支持：月考勤、周考勤、日考勤。"
        )

    return (
        f"部门：{department_name}\n"
        f"考勤类型：{attendance_type}\n"
        f"考勤结果：{result}"
    )


attendance_tool = FunctionTool(
    lookup_department,
    middlewares=[
        RequiredParamsMiddleware(),
    ],
    permission=PermissionDecision(
        behavior=PermissionBehavior.ALLOW,
        message="公司考勤查询属于只读操作，允许自动执行。",
    ),
)