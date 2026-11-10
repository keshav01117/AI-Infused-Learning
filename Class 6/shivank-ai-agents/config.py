"""Shared model configuration for every example in this masterclass.

Every example imports from here, so if a model is retired you change it
ONCE in this file instead of editing a dozen scripts.
"""

import os

# Current, non-retired models (verified working).
# The "us." prefix is a cross-region inference profile — required for Claude on Bedrock.
HAIKU = "us.anthropic.claude-haiku-4-5-20251001-v1:0"    # fast + cheap  → default
SONNET = "us.anthropic.claude-sonnet-4-5-20250929-v1:0"  # stronger reasoning
NOVA_LITE = "us.amazon.nova-lite-v1:0"                   # cheapest, Amazon's own

# Default used across the examples. Override with:  export MODEL_ID="..."
MODEL_ID = os.environ.get("MODEL_ID", HAIKU)

REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
