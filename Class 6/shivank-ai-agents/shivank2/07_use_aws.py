"""Module 2 · Lesson 7 — AWS integration with use_aws.

One tool, many services. use_aws translates plain English into AWS API calls.
You don't write boto3 code, don't handle AWS responses, and don't even
specify which operation to use. The agent works it out.

SAFETY: this script only does a READ-ONLY request (listing S3 buckets).
An empty list is a valid result, not an error.

use_aws CAN modify real resources. In a class, demo read-only requests only,
on a sandbox account.

    python shivank2/07_use_aws.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from strands import Agent
from strands.models.bedrock import BedrockModel
from strands_tools import use_aws
from config import MODEL_ID

agent = Agent(
    model=BedrockModel(model_id=MODEL_ID),
    tools=[use_aws],
    system_prompt="You are an AWS assistant that helps manage cloud resources.",
)

agent("List all S3 buckets in my account")

# Other examples (these need the resources to already exist):
#
# agent("Look up customer ID 12345 in the DynamoDB customers table "
#       "and update their email to newemail@example.com")
#
# agent("Invoke the Lambda function 'order-processor' with order ID 67890")
