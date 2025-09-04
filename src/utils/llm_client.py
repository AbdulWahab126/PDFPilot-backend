import os
from openai import OpenAI
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Get API key from env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def query_llm(prompt: str) -> str:
    """
    Send a prompt to OpenAI LLM and return its response
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4.1-mini" depending on your need
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"LLM query failed: {e}")
