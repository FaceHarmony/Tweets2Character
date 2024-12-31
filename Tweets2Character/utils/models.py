import os
from crewai import LLM

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

model_claude_sonnet = LLM(
  model="anthropic/claude-3-5-sonnet-20241022",
  api_key=ANTHROPIC_API_KEY,
  temperature=0.0
)

model_4o_mini = LLM(
  model="gpt-4o-mini",
  api_key=OPENAI_API_KEY,
  temperature=0.0
)

model_o1_mini = LLM(
  model="o1-mini",
  api_key=OPENAI_API_KEY,
  temperature=0.0
)

model_o1_preview = LLM(
  model="o1-preview",
  api_key=OPENAI_API_KEY,
  temperature=0.0
)
