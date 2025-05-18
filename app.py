import streamlit as st
import pandas as pd
import plotly.express as px

from wsagent.services import get_msgs_by_limit, msgs_agent
from wsagent.utils import rank_list
from wsagent.whatsapp import parse_whataspp

st.set_page_config(
    layout="wide", page_title="Analisador de Conversas do WhatsApp com IA"
)

# st.title("Análise de Conversas do WhatsApp com IA Gemini")

if "wsdata" not in st.session_state:
    st.session_state.wsdata = None
if "table" not in st.session_state:
    st.session_state.table = None
if "pie" not in st.session_state:
    st.session_state.pie = None
if "chat" not in st.session_state:
    st.session_state.chat = []
if "limit_days" not in st.session_state:
    st.session_state.limit_days = 1
if "zip_id" not in st.session_state:
    st.session_state.zip_id = None


with st.sidebar:
    st.header("1. Carregar Conversa")
    st.info("Exporte sua conversa do WhatsApp")
    zip_file = st.file_uploader(
        label="Selecione o arquivo da conversa (.zip)",
        type=["zip"],
        accept_multiple_files=False,
    )

    if zip_file:
        if zip_file.file_id != st.session_state.zip_id:
            st.session_state.chat = []
            st.session_state.zip_id = zip_file.file_id

        limit_days = st.number_input(
            "Quantidade de dias para filtrar:",
            min_value=1,
            max_value=90,
            step=1,
            value=st.session_state.limit_days,
        )
        if limit_days != st.session_state.limit_days:
            st.session_state.limit_days = limit_days
            with st.spinner("Processando arquivo..."):
                ws_data, ws_users = parse_whataspp(path=zip_file)
                _, users_count = get_msgs_by_limit(
                    ws_data=ws_data, limit_days=st.session_state.limit_days
                )

                st.session_state.wsdata = ws_data

                ranked = rank_list(raw_list=users_count, limit=10, index=1)

                top_df = pd.DataFrame(ranked, columns=["user", "count"])
                top_df["rank"] = top_df.reset_index(drop=True).index + 1
                top_df = top_df.set_index("rank")
                st.session_state.table = top_df

                if not st.session_state.table.empty:
                    st.session_state.pie = px.pie(
                        st.session_state.table,
                        values="count",
                        names="user",
                    )


col_chat, col_stats = st.columns([0.6, 0.4], gap="large")

with col_chat:
    st.header("2. Chatbot da Conversa")
    if st.session_state.table is None:
        st.info(
            "👈 Por favor, carregue um arquivo de conversa na barra lateral para iniciar o chat e ver as estatísticas."
        )
    else:
        with st.container(height=600):
            for msg in st.session_state.chat:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        if prompt := st.chat_input("Faça uma pergunta sobre a conversa..."):
            st.session_state.chat.append({"role": "user", "content": prompt})

            with st.spinner("Analisando e respondendo..."):
                resposta_bot = msgs_agent(
                    ws_data=st.session_state.wsdata,
                    limit_days=st.session_state.limit_days,
                    query=prompt,
                )
            st.session_state.chat.append({"role": "assistant", "content": resposta_bot})

            st.rerun()


with col_stats:
    st.header("3. Estatísticas da Conversa")
    if st.session_state.table is None:
        if not zip_file:
            st.info("👈 Carregue um arquivo para ver as estatísticas.")
        elif st.session_state.get("last_upload_id") is not None:
            st.write(
                "Nenhuma estatística para exibir (a conversa pode estar vazia ou não foi processada corretamente)."
            )
    else:
        st.plotly_chart(st.session_state.pie)
        st.table(st.session_state.table)
