# ============================================================
#  CLASS 1  —  From Your First API Call to a Live AI App
# ============================================================
#
#  What we'll build today, step by step:
#
#   Step 1 — Say hello to the OpenAI API
#   Step 2 — Swap in a free model using Groq
#   Step 3 — Scrape a website programmatically
#   Step 4 — Summarize it with GPT
#   Step 5 — Wrap everything in a shareable Gradio UI
#
#  Install everything you need:
#  pip install python-dotenv openai requests beautifulsoup4 gradio
# ============================================================


# ── STEP 1: Your first API call ─────────────────────────────
#
#  The openai library talks to GPT over the internet.
#  We never hardcode API keys in source files — instead we
#  store them in a .env file and load them at runtime.

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()           # reads OPENAI_API_KEY from .env

client = OpenAI()       # the key is picked up automatically

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a witty travel guide."},
        {"role": "user",   "content": "Suggest one thing to do in Bangalore."},
    ],
)
print("── GPT says:", response.choices[0].message.content)


# ── STEP 2: Same code, different brain (Groq + Llama) ───────
#
#  Groq exposes an OpenAI-compatible API, so we reuse the
#  exact same client — just point it at a different base_url
#  and swap in a free open-source model.  Zero new concepts.

import os

groq_client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a witty travel guide."},
        {"role": "user",   "content": "Suggest one thing to do in Bangalore."},
    ],
)
print("── Llama says:", response.choices[0].message.content)


# ── STEP 3: Give the model eyes — scrape a website ──────────
#
#  LLMs only know what's in their training data.  To summarize
#  a *live* page we fetch it ourselves, strip out noise
#  (scripts, navbars, footers), and hand the clean text to GPT.

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_website_contents(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Could not fetch the website. Error: {e}"

    soup = BeautifulSoup(r.text, "html.parser")
    title = soup.title.string if soup.title else "No title"

    for tag in soup(["script", "style", "nav", "footer", "header", "img", "input"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    return f"Title: {title}\n\nPage contents:\n{text}"


# ── STEP 4: Summarize the scraped content with GPT ──────────
#
#  Now we chain the two pieces together: fetch() → summarize().
#  The system prompt keeps the model focused on content,
#  and we ask for markdown so the output renders nicely later.

SYSTEM_PROMPT = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url):
    website = fetch_website_contents(url)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": f"Summarize this website:\n\n{website}"},
        ],
    )
    return response.choices[0].message.content


# ── STEP 5: Ship it — wrap everything in a Gradio UI ────────
#
#  Gradio turns a Python function into a web app in ~5 lines.
#  share=True gives you a public link you can send to anyone
#  without deploying anything — perfect for demos.

import gradio as gr

gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(label="Website URL"),
    outputs=gr.Markdown(label="Summary"),
    title="AI Website Summarizer",
).launch(share=True)
