import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv
from scraper import fetch_website_contents

load_dotenv(Path(__file__).resolve().parent / ".env")
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

system_prompt = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url):
    website = fetch_website_contents(url)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": f"Summarize this website:\n\n{website}"},
        ],
    )
    return response.choices[0].message.content
