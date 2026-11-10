"""Run this FIRST. Verifies your environment before you touch any example.

    python 00_check_setup.py
"""

import sys

OK, FAIL, WARN = "[ OK ]", "[FAIL]", "[WARN]"
problems = []


def check_python():
    v = sys.version_info
    if v >= (3, 10):
        print(f"{OK} Python {v.major}.{v.minor}")
    else:
        print(f"{FAIL} Python {v.major}.{v.minor} — need 3.10 or higher")
        problems.append("Install Python 3.10+")


def check_packages():
    for pkg, label in [("strands", "strands-agents"),
                       ("strands_tools", "strands-agents-tools"),
                       ("boto3", "boto3")]:
        try:
            __import__(pkg)
            print(f"{OK} {label} installed")
        except ImportError:
            print(f"{FAIL} {label} NOT installed")
            problems.append(f"pip install -r requirements.txt  (missing {label})")


def check_credentials():
    try:
        import boto3
        ident = boto3.client("sts").get_caller_identity()
        print(f"{OK} AWS credentials work — account {ident['Account']}")
        print(f"       identity: {ident['Arn']}")
    except Exception as e:
        msg = str(e)
        print(f"{FAIL} AWS credentials not working")
        if "ExpiredToken" in msg or "InvalidClientTokenId" in msg:
            problems.append("Credentials expired — paste a fresh block from the AWS "
                            "portal, or re-run 'aws configure'")
        else:
            problems.append("Set credentials: paste your SSO block, or run 'aws configure'")
        return False
    return True


def check_region():
    import os
    region = os.environ.get("AWS_DEFAULT_REGION")
    if region == "us-east-1":
        print(f"{OK} Region is us-east-1")
    elif region:
        print(f"{WARN} Region is '{region}' — examples assume us-east-1")
    else:
        print(f"{WARN} AWS_DEFAULT_REGION not set — run: export AWS_DEFAULT_REGION=us-east-1")


def check_bedrock():
    try:
        import boto3
        from config import MODEL_ID
        client = boto3.client("bedrock", region_name="us-east-1")
        models = client.list_foundation_models()["modelSummaries"]
        print(f"{OK} Bedrock reachable — {len(models)} models listed")

        # Can we actually CALL the default model?
        rt = boto3.client("bedrock-runtime", region_name="us-east-1")
        rt.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"text": "Say OK"}]}],
            inferenceConfig={"maxTokens": 10},
        )
        print(f"{OK} Model call succeeded — {MODEL_ID}")
    except Exception as e:
        msg = str(e)
        print(f"{FAIL} Bedrock problem: {type(e).__name__}")
        if "AccessDenied" in msg:
            problems.append("Enable model access: Bedrock console → Model access → "
                            "tick Claude Haiku 4.5 (region us-east-1)")
        elif "ResourceNotFound" in msg or "Legacy" in msg:
            problems.append("Model retired. Run: python 01_list_models.py, pick a live "
                            "one, and set it in config.py")
        else:
            problems.append(f"Bedrock error: {msg[:160]}")


print("=" * 62)
print("  Environment check — AI Agents on AWS, Modules 1 & 2")
print("=" * 62)
check_python()
check_packages()
check_region()
if check_credentials():
    check_bedrock()

print("-" * 62)
if problems:
    print("\nFIX THESE BEFORE CONTINUING:\n")
    for i, p in enumerate(problems, 1):
        print(f"  {i}. {p}")
    sys.exit(1)
else:
    print("\nAll checks passed. You're ready — start with:")
    print("    python shivank1/01_hello_world_agent.py\n")
