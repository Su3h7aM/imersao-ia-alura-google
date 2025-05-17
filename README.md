# WhatsApp CLI Chatbot

Este projeto fornece um chatbot em linha de comando (CLI) para explorar conversas exportadas do WhatsApp. A partir de um arquivo ZIP de exportação, o bot realiza análises, como ranking de usuários por volume de mensagens e detecção de sentimento, além de responder a consultas sobre o histórico de mensagens.

---

## Funcionalidades

* **Parser de exportação do WhatsApp**: Extrai e converte o `.zip` exportado em dados estruturados.
* **Top 10 Usuários Mais Ativos**: Gera uma tabela com os 10 usuários que mais enviaram mensagens, quantidade de mensagens e emoção predominante.
* **Agente de conversação**: Permite consultar o conteúdo das mensagens por período e obter respostas baseadas no histórico.
* **Detecção de sentimento**: Usa o agente de sentimento para classificar mensagens como `feliz`, `triste`, `engraçado`, etc.

## Requisitos

* Python 3.12 ou superior
* Dependências definidas em `pyproject.toml`:

  * `rich>=14.0.0`
  * `google-adk>=0.5.0`
  * `google-genai>=1.15.0`

Instale-as com:

```bash
uv sync
```

ou:

```bash
pip install -r requirements.txt
```

## Uso

1. **Prepare a exportação do WhatsApp**
   Exporte seu histórico de conversas do WhatsApp (`.zip`) e mova para `./data/`.

2. **Execute o script**

   ```bash
   uv run main.py
   ```

    ou:

   ```bash
   python main.py
   ```

3. **Interaja no CLI**

   * Informe o `Limite de dias` para filtrar o histórico.
   * O bot exibirá o **top 10 usuários**.
   * Digite sua pergunta sobre as conversas.
   * Digite `fim` para encerrar.

## Exemplo de Fluxo

```bash main.py
Limite de dias: 60
Top 10 Usuários mais ativos
┏━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━┓
┃Rank┃Usuário     ┃Mensagens  ┃Emoção     ┃
┡━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 1  │ Alice      │ 345       │ feliz     │
│ 2  │ Bruno      │ 298       │ engraçado │
│ …  │ …          │ …         │ …         │
└────┴────────────┴───────────┴───────────┘
Qual sua dúvida? quem enviou mais mensagens sobre o projeto?
> João enviou 27 mensagens falando sobre o projeto nos últimos 60 dias.
Prompt: fim
```
