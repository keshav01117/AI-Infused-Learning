"""Module 2 · Lesson 9 — Async tools (parallel execution).

THE PROBLEM:
Three warehouse lookups at 2 seconds each = 6 seconds if done one by one.

THE FIX:
Make the tool `async` and use agent.invoke_async(). The three calls run in
PARALLEL, so the whole thing takes about 2 seconds instead of 6.

WATCH THE PRINTED TIMING at the end — that IS the lesson.

    python shivank2/09_async_tools.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import time
from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from config import MODEL_ID


@tool
async def check_warehouse_inventory(product_id: str, warehouse: str) -> dict:
    """Check inventory at a specific warehouse.

    Args:
        product_id: Product ID to check
        warehouse: Warehouse identifier (e.g., "east", "west", "central")
    """
    # Simulate an API call delay
    await asyncio.sleep(2)

    data = {
        "east":    {"PROD-123": 45, "PROD-456": 12},
        "west":    {"PROD-123": 30, "PROD-456": 0},
        "central": {"PROD-123": 60, "PROD-456": 25},
    }

    quantity = data.get(warehouse, {}).get(product_id, 0)
    return {"warehouse": warehouse, "product_id": product_id, "quantity": quantity}


async def main():
    agent = Agent(
        model=BedrockModel(model_id=MODEL_ID),
        tools=[check_warehouse_inventory],
    )
    start = time.time()
    response = await agent.invoke_async(
        "Can we ship 100 units of PROD-123? Check all warehouses: east, west, and central."
    )
    elapsed = time.time() - start
    print(response.message["content"][0]["text"])
    print(f"\nTotal time: {elapsed:.1f}s (sequential would be ~6s)")


if __name__ == "__main__":
    # In a script use asyncio.run(). In a Jupyter cell, just: await main()
    asyncio.run(main())
