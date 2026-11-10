"""Module 2 · Lesson 3 — When one tool isn't enough.

"Pull last quarter's sales data and email a summary to the team" is not one
task. It's three: query, analyse, send.

You give the agent three small tools. You NEVER tell it the order.
It works out: get data -> analyse it -> email the result. That's planning.

    python shivank2/03_multi_tool_sales.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from config import MODEL_ID


@tool
def get_sales_data(quarter: str) -> dict:
    """Retrieve sales data for a specific quarter."""
    return {"revenue": 1250000, "deals": 47, "quarter": quarter}


@tool
def analyze_sales(revenue: int, deals: int, quarter: str) -> str:
    """Calculate key metrics from sales data."""
    avg_deal = revenue / deals
    return f"Q{quarter}: ${revenue:,} revenue, {deals} deals, ${avg_deal:,.0f} avg deal size"


@tool
def send_email(to: str, subject: str, body: str) -> str:
    """Send an email message."""
    return f"Email sent to {to}"


agent = Agent(
    model=BedrockModel(model_id=MODEL_ID),
    tools=[get_sales_data, analyze_sales, send_email],
)

response = agent("Pull last quarter's sales data and email a summary to the team")

# RULE OF THUMB: build focused, single-purpose tools.
# One mega-tool that does everything is harder to maintain, harder for the
# agent to reason about, and impossible to reuse elsewhere.
