from google import genai
from google.genai import types

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService

gemini = genai.Client()

APP_NAME = "wsagent"
USER_ID = "user_1"
SESSION_ID = "session_1"

session_service = InMemorySessionService()

session = session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)


# def call_agent(query: str, runner, user_id, session_id):
def call_agent(agent: Agent, query: str):
    content = types.Content(role="user", parts=[types.Part(text=query)])

    response = ""

    runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)

    for event in runner.run(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        if event.is_final_response():
            for part in event.content.parts:
                if part.text is not None:
                    response += part.text
                    response += "\n"
        return response
