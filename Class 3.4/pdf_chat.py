"""A small RAG app for asking questions about an uploaded PDF."""

import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


load_dotenv(Path(__file__).resolve().parent.parent / ".env")

prompt = ChatPromptTemplate.from_template(
    """
You are a helpful PDF assistant. Answer the question using ONLY the context below.
If the context does not contain the answer, say "I couldn't find that in the document."
After your answer, list the page numbers you used as: Sources: page X, page Y.

Context:
{context}

Question: {question}
"""
)

state = {"db": None}


def get_model():
    if not os.getenv("GEMINI_API_KEY"):
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Add it to the repository .env file, then restart the app."
        )
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        google_api_key=os.environ["GEMINI_API_KEY"],
    )


def build_index(pdf_path):
    pages = PyPDFLoader(pdf_path).load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(pages)
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma.from_documents(chunks, embedder)


def upload(pdf):
    if pdf is None:
        return "Please choose a PDF first."

    try:
        state["db"] = build_index(pdf.name if hasattr(pdf, "name") else pdf)
    except Exception as error:
        state["db"] = None
        return f"Could not index the PDF: {error}"

    return "PDF indexed. Ask me anything about it."


def ask(db, question):
    chunks = db.similarity_search(question, k=4)
    context = "\n\n".join(
        f"[page {chunk.metadata['page'] + 1}] {chunk.page_content}"
        for chunk in chunks
    )
    chain = prompt | get_model()
    return chain.invoke({"context": context, "question": question}).content


def chat(message, history):
    del history
    if state["db"] is None:
        return "Please upload a PDF first."
    try:
        return ask(state["db"], message)
    except RuntimeError as error:
        return str(error)


with gr.Blocks(title="Chat with your PDF") as demo:
    gr.Markdown("## Chat with your PDF")
    pdf = gr.File(label="Upload a PDF", file_types=[".pdf"], type="filepath")
    status = gr.Markdown()
    pdf.upload(upload, inputs=pdf, outputs=status)
    gr.ChatInterface(fn=chat)


if __name__ == "__main__":
    demo.launch()