"""Module 2 · Lesson 6 — Combining several pre-built tools.

Fetch data from the web, do maths on it, save a file — one request, three tools.

ABOUT BYPASS_TOOL_CONSENT:
Some tools are sensitive (they write files, touch cloud resources), so Strands
PAUSES and asks your permission before running them. Setting this to "true"
turns that prompt off so the script runs unattended.

That prompt is a real safety feature — in production you often WANT a human
approving actions. If a script ever seems to hang, it's probably waiting for
you to type 'y'.

    python shivank2/06_multi_prebuilt_tools.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import http_request, calculator, file_write
from config import MODEL_ID

agent = Agent(
    model=BedrockModel(model_id=MODEL_ID),
    tools=[http_request, calculator, file_write],
    system_prompt="You help with data analysis tasks.",
)

os.environ["BYPASS_TOOL_CONSENT"] = "true"

agent("""
Fetch stock data from https://query1.finance.yahoo.com/v8/finance/chart/AAPL?interval=1d&range=5d,
extract the latest closing prices,
calculate the average price over the period,
and save the results to stock_summary.txt
""")
