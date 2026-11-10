"""Module 2 · Lesson 1 — From a plain function to a tool.

THE CORE IDEA OF MODULE 2.

A normal Python function is invisible to an agent. To expose it, add 3 things:
    1. the @tool decorator   -> makes it available to agents
    2. type hints            -> tells the agent what data types to expect
    3. a proper docstring    -> tells the agent WHEN to use it

    python shivank2/01_function_to_tool.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from config import MODEL_ID


@tool                                              # 1. decorator
def check_server_status(server_url: str) -> str:   # 2. type hints
    """Check if a server is responding by making an HTTP request.

    Args:
        server_url: The URL of the server to check

    Returns:
        A message indicating whether the server is up or down
    """                                            # 3. docstring
    try:
        response = requests.get(server_url, timeout=5)
        return f"Server is up. Status code: {response.status_code}"
    except requests.exceptions.RequestException:
        return "Server is down or unreachable"


agent = Agent(model=BedrockModel(model_id=MODEL_ID), tools=[check_server_status])

response = agent("Is the staging server running? Check https://httpbin.org/get")

# ---------------------------------------------------------------------------
# TRY THIS EXPERIMENT (the best 2 minutes in this whole module):
# Change the docstring above to just  """Does a thing."""  and re-run.
# The agent will often STOP calling the tool.
# Why? The docstring is not a comment — it is the manual the MODEL reads
# to decide whether your tool is relevant. Vague docstring = unreliable agent.
# ---------------------------------------------------------------------------
