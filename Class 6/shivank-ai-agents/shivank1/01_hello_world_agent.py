"""Module 1 · Lesson 1 — The simplest possible agent (Strands + Bedrock).

Four lines is a whole agent:
  1. choose a model
  2. wrap it in an Agent
  3. call the agent like a function
  4. print the answer

There are no tools here, so the agentic loop runs exactly once.
This is the "before" picture for Module 2.

    python shivank1/01_hello_world_agent.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent
from strands.models.bedrock import BedrockModel
from config import NOVA_LITE

# Nova Lite: Amazon's cheapest model — ideal for a first run.
model = BedrockModel(model_id=NOVA_LITE)

agent = Agent(model=model)

response = agent("Hello! Tell me a fun fact about AI agents.")
print(response)
