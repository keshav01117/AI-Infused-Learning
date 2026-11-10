"""Module 2 · Lesson 8 — Class-based tools (the shared-resource pattern).

THE PROBLEM:
Your DBA messages you: "Why is your agent opening 50 database connections
per minute?" Each @tool function opened its own connection. Five tools =
five connections per request. Multiply by concurrent users -> the DB drowns.

THE FIX:
Group related tools in a class. They share ONE connection (here, one dict)
via self, created once in __init__.

    python shivank2/08_class_based_tools.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent, tool
from strands.models.bedrock import BedrockModel
from config import MODEL_ID


class InventoryTools:
    def __init__(self):
        # Shared resource: all tools access the same data store.
        # In production: self.db = connect_to_database()   <-- opened ONCE
        self.products = {
            "PROD-123": {"name": "Wireless Mouse", "quantity": 15, "price": 29.99},
            "PROD-456": {"name": "USB-C Hub", "quantity": 0, "price": 49.99},
            "PROD-789": {"name": "Mechanical Keyboard", "quantity": 8, "price": 89.99},
        }

    @tool
    def check_stock(self, product_id: str) -> str:
        """Check product stock level.

        Args:
            product_id: The product ID to check
        """
        product = self.products.get(product_id)
        if not product:
            return f"Product {product_id} not found"
        return f"{product['name']}: {product['quantity']} units at ${product['price']}"

    @tool
    def update_stock(self, product_id: str, quantity: int) -> str:
        """Update product stock quantity.

        Args:
            product_id: The product ID to update
            quantity: New quantity to set
        """
        if product_id in self.products:
            self.products[product_id]["quantity"] = quantity
            return f"Updated {product_id} to {quantity} units"
        return f"Product {product_id} not found"


# One instance, shared state, multiple tools
inventory = InventoryTools()
agent = Agent(
    model=BedrockModel(model_id=MODEL_ID),
    tools=[inventory.check_stock, inventory.update_stock],
)

agent("Check stock for PROD-123")
agent("Update PROD-456 stock to 25 units, then confirm the new level")

# Note the second request: the agent UPDATES then RE-CHECKS, and the change
# persists because both tools share the same self.products.
