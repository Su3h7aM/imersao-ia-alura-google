import json

from google.adk.tools import FunctionTool

from wsagent.gemini import call_agent
from wsagent.agents import sentiment_extractor
from wsagent.tools import get_user_msg


user_msgs_tool = FunctionTool(func=get_user_msg)


def get_user_sentiment(ws_data, user, limit_days):
    user_msgs = get_user_msg(ws_data=ws_data, user=user, limit_days=limit_days)

    msg_text = ""

    for msg in user_msgs:
        msg_text += (
            f"{msg['date']} - {msg['time']} -> {msg['user']}: {msg['message']}\n"
        )

    response = call_agent(agent=sentiment_extractor, query=msg_text)

    if response is not None:
        sentiment = json.loads(response)

        return sentiment["sentiment"]


def msgs_agent():
    pass
