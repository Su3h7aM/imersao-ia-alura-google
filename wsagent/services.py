import json
from datetime import datetime

from wsagent.gemini import call_agent
from wsagent.agents import sentiment_extractor
from wsagent.agents import conversational_agent

now = datetime.now()


def get_msgs_by_limit(ws_data, limit_days):
    msgs = []
    counts = {}

    for entry in ws_data:
        delta = now - datetime.strptime(entry["date"], "%m/%d/%y")
        if delta.days <= limit_days:
            msgs.append(entry)

            user = entry["user"]
            if user not in counts:
                counts[user] = 0
            counts[user] += 1

    return msgs, counts


def get_user_msgs(ws_data, user, limit_days):
    user_msgs = []

    limited_msgs, _ = get_msgs_by_limit(ws_data=ws_data, limit_days=limit_days)

    for entry in limited_msgs:
        if entry["user"] == user:
            user_msgs.append(entry)

    return user_msgs


def get_user_sentiment(ws_data, user: str, limit_days: int):
    user_msgs = get_user_msgs(ws_data=ws_data, user=user, limit_days=limit_days)

    msg_text = ""

    for msg in user_msgs:
        msg_text += (
            f"{msg['date']} - {msg['time']} -> {msg['user']}: {msg['message']}\n"
        )

    response = call_agent(agent=sentiment_extractor, query=msg_text)

    if response is not None:
        sentiment = json.loads(response)

        return sentiment["sentiment"]


def msgs_agent(ws_data, limit_days: int, query: str):
    limited_msgs, _ = get_msgs_by_limit(ws_data=ws_data, limit_days=limit_days)

    msg_text = ""

    for msg in limited_msgs:
        msg_text += (
            f"{msg['date']} - {msg['time']} -> {msg['user']}: {msg['message']}\n"
        )

    call_agent(agent=conversational_agent, query=msg_text)
    chat = call_agent(agent=conversational_agent, query=query)

    return chat
