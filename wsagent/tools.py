from datetime import datetime


def get_user_msg(ws_data, user, limit_days):
    """ """
    user_msgs = []

    now = datetime.now()

    for entry in ws_data:
        delta = now - datetime.strptime(entry["date"], "%m/%d/%y")
        if delta.days <= limit_days and entry["user"] == user:
            user_msgs.append(entry)

    return user_msgs
