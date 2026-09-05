import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY was not found in .env")

model = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1",
    temperature=0,
)
