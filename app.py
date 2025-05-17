import streamlit as st
import pandas as pd
import plotly.express as px

from wsagent.services import get_msgs_by_limit
from wsagent.utils import rank_list
from wsagent.whatsapp import parse_whataspp

st.set_page_config(
    layout="wide", page_title="Analisador de Conversas do WhatsApp com IA"
)

st.title("Análise de Conversas do WhatsApp com IA Gemini")

if "chat" not in st.session_state:
    st.session_state.chat = None
if "table" not in st.session_state:
    st.session_state.table = None
if "pie" not in st.session_state:
    st.session_state.pie = None

with st.sidebar:
    st.header("1. Carregar Conversa")
    st.info("Exporte sua conversa do WhatsApp")
    zip_file = st.file_uploader(
        label="Selecione o arquivo da conversa (.zip)",
        type=["zip"],
        accept_multiple_files=False,
    )

    if zip_file:
        with st.spinner("Processando arquivo..."):
            ws_data, ws_users = parse_whataspp(path=zip_file)
            _, users_count = get_msgs_by_limit(ws_data=ws_data, limit_days=30)

            ranked = rank_list(raw_list=users_count, limit=10, index=1)

            st.session_state.table = pd.DataFrame(ranked, columns=["user", "count"])
            st.session_state.full_table = pd.DataFrame(
                ws_data, columns=["date", "time", "user", "message"]
            )

            if not st.session_state.table.empty:
                st.session_state.pie = px.pie(
                    st.session_state.table,
                    values="count",
                    names="user",
                    title="Distribuição de Mensagens por Usuário",
                )


col_chat, col_stats = st.columns([0.6, 0.4])

with col_chat:
    st.header("2. Chatbot da Conversa")
    if st.session_state.table is None:  # or st.session_state.chat.empty:
        st.info(
            "👈 Por favor, carregue um arquivo de conversa na barra lateral para iniciar o chat e ver as estatísticas."
        )
    else:
        pass

with col_stats:
    st.header("3. Estatísticas da Conversa")
    if st.session_state.table is None:  # or st.session_state.table.empty:
        if not zip_file:  # Se nenhum arquivo foi sequer tentado
            st.info("👈 Carregue um arquivo para ver as estatísticas.")
        elif st.session_state.get("last_upload_id") is not None:
            st.write(
                "Nenhuma estatística para exibir (a conversa pode estar vazia ou não foi processada corretamente)."
            )
    else:
        st.plotly_chart(st.session_state.pie)
        st.table(st.session_state.table)
