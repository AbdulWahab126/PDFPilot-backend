import os
from openai import OpenAI
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Get API key from env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing in environment variables")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def query_llm(prompt: str) -> str:
    """
    Send a prompt to Groq LLM and return its response
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # or "gpt-4.1-mini" depending on your need
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"LLM query failed: {e}")
