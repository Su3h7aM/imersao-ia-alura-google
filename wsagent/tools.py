from google.adk.tools import FunctionTool

from wsagent.services import get_user_msg

user_msgs_tool = FunctionTool(func=get_user_msg)
