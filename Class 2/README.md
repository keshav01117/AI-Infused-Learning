# AI Engineering · Class 2 — LangChain & Your First Agent (runnable code)

Every file here matches a code block from the Class 2 deck. They are
self-contained — run any one of them directly.

## One-time setup
```bash
# 1. create & activate a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. install everything
pip install -r requirements.txt

# 3. add your key
#    copy .env.example to a file named .env, then paste your OpenAI key inside
cp .env.example .env            # Windows: copy .env.example .env
```
Get a key at https://platform.openai.com/api-keys (add a little billing credit).

## What we learned

- LangChain separates prompts, models, and output parsers into reusable steps.
- The `|` operator composes those steps into a runnable chain.
- Conversation memory is implemented by sending previous `HumanMessage` and `AIMessage` objects with each request.
- An agent lets an LLM decide when to call a Python function (tool), then uses the tool result to form its answer.
- Function tools need a name, description, parameter schema, and a tool-result message linked by `tool_call_id`.
- A shared provider factory keeps API keys, model names, and API endpoints in one place.
- The same OpenAI-compatible client can use OpenAI or Groq by changing the key, endpoint, and model.
- Gradio turns the agent function into a browser-based chat interface.
- Website summarization combines the Class 1 scraper with a LangChain prompt/model/parser chain.

## What to run (in deck order)
| File | What it shows | Run |
|------|---------------|-----|
| `scraper.py` | Class 1 helper: URL -> page text | `python scraper.py` |
| `summarizer_langchain.py` | Block 10 — summarizer rebuilt in LangChain (prompt \| model \| parser) | `python summarizer_langchain.py` |
| `memory_demo.py` | Block 10 — memory with history typed by hand | `python memory_demo.py` |
| `memory_chat.py` | Block 10 — memory that builds itself in a chat loop | `python memory_chat.py` |
| `agent.py` | Block 11 — your first tool-using agent | `python agent.py` |
| `app.py` | Block 12 — the agent with a Gradio chat UI + public link | `python app.py` |

## Notes
- The shared provider prefers `OPENAI_API_KEY` in `Class2/.env` and falls back to `GROQ_API_KEY` in `class 1/.env`.
- The OpenAI setup uses `gpt-4o-mini`; the Groq fallback uses `GROQ_MODEL` or `openai/gpt-oss-20b`.
- `summarizer_langchain.py` imports `fetch_website_contents` from `scraper.py`,
  so keep them in the same folder.
- `app.py` imports `agent` from `agent.py` — same folder.
- Never commit `.env`. A `.gitignore` is included that already ignores it.

## Stop a running app
Press `Ctrl + C` in the terminal.
