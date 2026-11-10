"""Module 2 · Lesson 4 — Building a custom tool.

When community tools don't fit (internal API, proprietary database), you
write your own. Here: an online store checking stock.

The mock dictionary stands in for a real database. The agent-facing part —
decorator, type hints, docstring — is identical either way.

    python shivank2/04_custom_tool_inventory.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from config import MODEL_ID


@tool
def check_inventory(product_id: str) -> str:
    """Check if a product is in stock.

    Args:
        product_id: The product ID to check (e.g., "PROD-123")
    """
    # In production you'd query your real database here.
    inventory = {
        "PROD-123": 15,
        "PROD-456": 0,
        "PROD-789": 8,
    }

    quantity = inventory.get(product_id, 0)

    if quantity > 0:
        return f"Product {product_id} is in stock. We have {quantity} units available."
    else:
        return f"Product {product_id} is currently out of stock."


agent = Agent(model=BedrockModel(model_id=MODEL_ID), tools=[check_inventory])

# All of these work — the agent understands intent, not just keywords
agent("Is PROD-123 in stock?")
agent("Do we have PROD-456 available?")
agent("Check inventory for PROD-789")
agent("Can I order PROD-123 right now?")

# ---------------------------------------------------------------------------
# YOUR TURN (exercise). Build a tool for something you care
# about. Ideas: check the weather in your city (call a weather API) /
# validate an email format / calculate age from a birthdate / calculate BMI /
# calculate shipping cost from weight + distance.
# Don't worry if the logic is simple — the point is seeing how a custom tool
# fits into the agent workflow.
# ---------------------------------------------------------------------------
