from typing import Literal
from pydantic import BaseModel

from google.adk.agents import Agent


MODEL = "gemini-2.0-flash"


class UserSentiment(BaseModel):
    sentiment: Literal["negativo", "positivo", "neutro", "engraçado"]


sentiment_extractor = Agent(
    name="sentiment_extractor",
    model=MODEL,
    description="Agente para extrair sentimentos de conversas",
    instruction="",
    output_schema=UserSentiment,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

conversational_agent = Agent(
    name="conversational_agent",
    model=MODEL,
    description="Agente principal para conversas",
    instruction="",
    tools=[],
)
