from pathlib import Path

from agentscope.skill import LocalSkillLoader


# =========================
# Skill 根目录
# =========================

SKILLS_DIR = (
    Path(__file__)
    .resolve()
    .parent
    / "skills"
)


print("SKILLS_DIR =", SKILLS_DIR)
print("skills exists =", SKILLS_DIR.exists())
print("skills is_dir =", SKILLS_DIR.is_dir())


# =========================
# Skill Loader
# =========================

skill_loader = LocalSkillLoader(
    directory=str(SKILLS_DIR),
    scan_subdir=True,
)


# from pathlib import Path
#
# from agentscope.tool import Toolkit
#
# from tools_collection.weather import weather_tool
#
#
# from pathlib import Path
#
# SKILLS_DIR = (
#     Path(__file__)
#     .resolve()
#     .parent
#     / "skills"
# )
#
# print("SKILLS_DIR =", SKILLS_DIR)
# print("skills exists =", SKILLS_DIR.exists())
# print("skills is_dir =", SKILLS_DIR.is_dir())
#
#
# # 当前文件：
# # invokeLocalAi/skills_collection/skill_loader.py
# #
# # Skill 根目录：
# # invokeLocalAi/skills_collection/skills/
#
# SKILLS_DIR = (
#     Path(__file__)
#     .resolve()
#     .parent
#     / "skills"
# )
#
#
# def create_toolkit() -> Toolkit:
#     """创建 Agent 使用的统一 Toolkit。
#
#     Toolkit 中统一加载：
#     1. Python Tools
#     2. AgentScope Skills
#
#     后续还可以继续添加：
#     3. MCP
#     4. 其他 Tool
#     """
#
#     toolkit = Toolkit(
#
#         # 普通 Tool
#         tools=[
#             weather_tool,
#         ],
#
#         # Skill 根目录
#         skills_or_loaders=[
#             str(SKILLS_DIR),
#         ],
#     )
#
#     return toolkit
#
#
# # 默认 Toolkit
# toolkit = create_toolkit()