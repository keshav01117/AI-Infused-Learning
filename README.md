# AI-Infused-Learning

## Class 1: Short Revision Notes

### What we learned

- Use the `openai` Python package to call an LLM from Python.
- Keep API keys in `.env`; never hardcode or commit them.
- Use `python-dotenv` to load environment variables at runtime.
- Groq provides an OpenAI-compatible API. Change `base_url`, API key, and model to use it.
- Use `requests` and `BeautifulSoup` to fetch and clean website content.
- Send the cleaned content to an LLM with a clear system prompt to generate a summary.
- Use Gradio to turn a Python function into a simple shareable web app.

### Core API pattern

```python
from openai import OpenAI

client = OpenAI(api_key="...", base_url="https://api.groq.com/openai/v1")

response = client.chat.completions.create(
	model="your-model",
	messages=[
		{"role": "system", "content": "You are a helpful assistant."},
		{"role": "user", "content": "Your question"},
	],
)
print(response.choices[0].message.content)
```

### Class 1 flow

`fetch website -> clean HTML -> summarize content -> display with Gradio`

### Setup and run

```bash
pip install python-dotenv openai requests beautifulsoup4 gradio
python "class 1/first_class.py"
```

Add the required provider key to `.env`, for example `GROQ_API_KEY=your-key`.

## Class 2: LangChain and Agents

### What we learned

- LangChain separates prompts, models, and output parsers into reusable steps.
- The `|` operator composes those steps into a runnable chain.
- Conversation memory sends previous `HumanMessage` and `AIMessage` objects with each request.
- An agent lets an LLM decide when to call a Python function, then uses the tool result to answer.
- Function tools need a name, description, parameter schema, and a result linked by `tool_call_id`.
- A shared provider factory keeps API keys, model names, and API endpoints in one place.
- The same OpenAI-compatible client can use OpenAI or Groq by changing the key, endpoint, and model.
- Gradio turns the agent function into a browser-based chat interface.
- Website summarization combines the Class 1 scraper with a LangChain prompt/model/parser chain.

### Class 2 flow

`prompt -> model -> parser`  |  `agent -> tool call -> tool result -> final answer`

### Setup and run

```bash
pip install -r "Class2/requirements.txt"
python "Class2/summarizer_langchain.py"
python "Class2/agent.py"
```

Class 2 prefers `OPENAI_API_KEY` in `Class2/.env` and falls back to
`GROQ_API_KEY` in `class 1/.env`. Never commit `.env` files.