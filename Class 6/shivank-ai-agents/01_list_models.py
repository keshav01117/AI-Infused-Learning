"""List the Bedrock models available in your account.

Use this whenever you hit a retired-model error:
    ResourceNotFoundException ... end of its life
    ... marked by provider as Legacy

Pick a live model from this list, add the "us." prefix, and set it in config.py.

    python 01_list_models.py
"""

import boto3

REGION = "us-east-1"
client = boto3.client("bedrock", region_name=REGION)
models = client.list_foundation_models()["modelSummaries"]

wanted = ("anthropic.claude", "amazon.nova")
seen = set()

print(f"\nModels available in {REGION}\n" + "=" * 56)
for m in models:
    mid = m["modelId"]
    if any(w in mid for w in wanted) and mid not in seen:
        seen.add(mid)
        print(f"  {mid}")

print("\nTo call these from code, prefix with 'us.' — for example:")
print("  us.anthropic.claude-haiku-4-5-20251001-v1:0")
print("\nSet your choice in config.py (MODEL_ID), or:")
print("  export MODEL_ID='us.anthropic.claude-haiku-4-5-20251001-v1:0'\n")
