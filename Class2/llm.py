import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from openai import OpenAI


CLASS2_DIR = Path(__file__).resolve().parent


def get_provider_config():
    load_dotenv(CLASS2_DIR / ".env")

    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and "xxxx" not in openai_key.lower():
        return {
            "api_key": openai_key,
            "model": "gpt-4o-mini",
            "base_url": None,
        }

    load_dotenv(CLASS2_DIR.parent / "class 1" / ".env")
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and "xxxx" not in groq_key.lower():
        return {
            "api_key": groq_key,
            "model": os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
            "base_url": "https://api.groq.com/openai/v1",
        }

    raise RuntimeError(
        "No valid API key found. Add OPENAI_API_KEY to Class2/.env or "
        "GROQ_API_KEY to class 1/.env."
    )


def create_openai_client():
    config = get_provider_config()
    options = {"api_key": config["api_key"]}
    if config["base_url"]:
        options["base_url"] = config["base_url"]
    return OpenAI(**options)


def create_chat_model(**options):
    config = get_provider_config()
    model_options = {
        "model": config["model"],
        "api_key": config["api_key"],
        **options,
    }
    if config["base_url"]:
        model_options["base_url"] = config["base_url"]
    return ChatOpenAI(**model_options)
