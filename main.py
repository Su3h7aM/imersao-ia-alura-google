from wsagent.whatsapp import parse_whataspp
from wsagent.services import get_user_sentiment

ws_data, ws_users = parse_whataspp("./data/WhatsApp Chat with 1RI Forever.zip")


teste = get_user_sentiment(ws_data=ws_data, user="Cezar Nilo Hoffmann", limit_days=1)

print(teste)
