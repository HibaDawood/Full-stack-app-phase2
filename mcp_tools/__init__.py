from .add_task_tool import add_task
from .update_task_tool import update_task
from .read_tasks_tool import read_tasks
from .delete_task_tool import delete_task
from .complete_task_tool import complete_task

# Dictionary mapping tool names to their functions
TOOLS_MAP = {
    "add_task": add_task,
    "update_task": update_task,
    "read_tasks": read_tasks,
    "delete_task": delete_task,
    "complete_task": complete_task
}

def execute_tool(tool_name: str, **kwargs):
    """
    Execute a tool by name with the provided arguments
    """
    if tool_name in TOOLS_MAP:
        return TOOLS_MAP[tool_name](**kwargs)
    else:
        return {
            "success": False,
            "message": f"Unknown tool: {tool_name}"
        }