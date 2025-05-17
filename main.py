from rich.console import Console
from rich.markdown import Markdown

from wsagent.whatsapp import parse_whataspp
from wsagent.services import msgs_agent
from wsagent.utils import print_top10

ws_data, ws_users = parse_whataspp("./data/WhatsApp Chat with 1RI Forever.zip")

console = Console()

print_top10(console=console, ws_data=ws_data, limit_days=30)

limit = input("Limite de dias: ")
limit = int(limit)

user_msg = input("Qual sua dúvida? ")

while user_msg != "fim":
    response = msgs_agent(ws_data=ws_data, limit_days=limit, query=user_msg)
    if response is not None:
        formated = Markdown(response)
        console.print(formated)
        user_msg = input("Prompt: ")
