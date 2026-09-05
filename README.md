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
python first_class.py
```

Add the required provider key to `.env`, for example `GROQ_API_KEY=your-key`.