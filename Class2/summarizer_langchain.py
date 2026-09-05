# summarizer_langchain.py
# Block 10 — your Class 1 summarizer, rebuilt the LangChain way.
# Run:  python summarizer_langchain.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from llm import create_chat_model
from scraper import fetch_website_contents   # reuse Class 1's scraper

# ① a reusable prompt with a {website} blank
prompt = ChatPromptTemplate.from_template(
    "Give a short, friendly summary of this website:\n\n{website}"
)

# ② the same model from Class 1, wrapped for LangChain
model = create_chat_model(temperature=0.3)

# ③ the package-opener: hands back plain text
parser = StrOutputParser()

# ④ snap them together  (| means "then")
chain = prompt | model | parser


def summarize(url):
    # ⑤ run it; the dict fills the {website} blank by name
    return chain.invoke({"website": fetch_website_contents(url)})


if __name__ == "__main__":
    print(summarize("https://anthropic.com"))
