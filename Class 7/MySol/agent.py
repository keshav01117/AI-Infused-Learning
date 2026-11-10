"""InterviewIQ: a Grok-powered interview coach with a Streamlit browser UI.

Setup:
	pip install streamlit openai
	set GROK_API_KEY=your_xai_api_key   # PowerShell: $env:GROK_API_KEY="..."
	streamlit run agent.py
"""

import json
import os
import re
from typing import Any


def detect_filler_words(answer: str) -> dict[str, Any]:
	"""Find common spoken fillers and report their counts and locations."""
	fillers = ("um", "uh", "er", "ah", "like", "basically", "actually", "literally", "you know", "I mean")
	found: dict[str, int] = {}
	for filler in fillers:
		pattern = rf"(?<!\w){re.escape(filler)}(?!\w)"
		count = len(re.findall(pattern, answer, flags=re.IGNORECASE))
		if count:
			found[filler] = count
	total = sum(found.values())
	return {
		"tool": "detect_filler_words",
		"filler_counts": found,
		"total_count": total,
		"has_filler_words": total > 0,
		"feedback": "Try replacing fillers with a brief pause." if total else "No common filler words detected.",
	}


def check_star_structure(answer: str) -> dict[str, Any]:
	"""Estimate whether a behavioral answer includes each STAR component."""
	patterns = {
		"Situation": r"\b(when|while|during|at the time|in my|on the project|our team|the context)\b",
		"Task": r"\b(my (task|role|goal|responsibility)|I (needed|had|was responsible|was asked) to|the challenge|our goal)\b",
		"Action": r"\b(I (?:[a-z]+ed|built|created|led|implemented|organized|analyzed|decided|developed|coordinated)|my approach|we (?:built|created|implemented))\b",
		"Result": r"\b(result(?:ed)?|outcome|impact|achieved|increased|reduced|improved|saved|delivered|learned|by \d+)\b",
	}
	components = {name: bool(re.search(pattern, answer, re.IGNORECASE)) for name, pattern in patterns.items()}
	covered = sum(components.values())
	missing = [name for name, present in components.items() if not present]
	return {
		"tool": "check_star_structure",
		"components": components,
		"covered_count": covered,
		"missing_components": missing,
		"complete": not missing,
		"feedback": "All four STAR elements are present." if not missing else f"Consider adding: {', '.join(missing)}.",
	}


_STOPWORDS = {
	"about", "after", "again", "against", "also", "answer", "being", "between", "could", "during",
	"each", "from", "have", "into", "interview", "more", "most", "other", "over", "question", "should",
	"tell", "than", "that", "their", "there", "these", "they", "this", "those", "through", "under", "very",
	"what", "when", "where", "which", "while", "with", "would", "your", "you", "were", "will", "work",
	"describe", "explain", "share", "give", "example", "experience", "time", "handled", "manage", "managed",
}


def score_relevance(question: str, answer: str, expected_keywords: list[str] | None = None) -> dict[str, Any]:
	"""Score coverage of question concepts; callers may supply expected concepts."""
	if expected_keywords:
		keywords = list(dict.fromkeys(k.strip() for k in expected_keywords if k and k.strip()))
	else:
		keywords = [
			word for word in dict.fromkeys(re.findall(r"[a-zA-Z][a-zA-Z'-]{2,}", question.lower()))
			if word not in _STOPWORDS
		]
	answer_lower = answer.lower()
	matched = [keyword for keyword in keywords if re.search(rf"(?<!\w){re.escape(keyword.lower())}(?!\w)", answer_lower)]
	missing = [keyword for keyword in keywords if keyword not in matched]
	score = round(100 * len(matched) / len(keywords)) if keywords else 0
	return {
		"tool": "score_relevance",
		"score": score,
		"matched_keywords": matched,
		"missing_keywords": missing,
		"keywords_checked": keywords,
		"feedback": "Strong coverage of the question's key concepts." if score >= 70 else "Add more specific details tied to the question.",
	}


TOOLS = [
	{
		"type": "function",
		"function": {
			"name": "detect_filler_words",
			"description": "Detect common filler words in a candidate's spoken answer.",
			"parameters": {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]},
		},
	},
	{
		"type": "function",
		"function": {
			"name": "check_star_structure",
			"description": "Check whether a behavioral interview answer covers Situation, Task, Action, and Result.",
			"parameters": {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]},
		},
	},
	{
		"type": "function",
		"function": {
			"name": "score_relevance",
			"description": "Score how well an answer covers the expected concepts for its interview question. Supply concise expected keywords/concepts.",
			"parameters": {
				"type": "object",
				"properties": {
					"question": {"type": "string"},
					"answer": {"type": "string"},
					"expected_keywords": {"type": "array", "items": {"type": "string"}},
				},
				"required": ["question", "answer"],
			},
		},
	},
]

TOOL_FUNCTIONS = {
	"detect_filler_words": detect_filler_words,
	"check_star_structure": check_star_structure,
	"score_relevance": score_relevance,
}

SYSTEM_PROMPT = """You are InterviewIQ, an encouraging and concise mock-interview coach. Evaluate the candidate's answer, not the candidate as a person. For an answer evaluation, call detect_filler_words and score_relevance; call check_star_structure when the question is behavioral or asks for an experience/example. For relevance, infer a short list of concrete expected concepts from the question and pass them to the tool. Use the tool results accurately, then give brief, specific, constructive feedback and one practical next step. Do not invent facts. The entire conversation is available as session memory; use it to answer follow-up questions about earlier answers and feedback. If the user asks a general session question, answer from the conversation without unnecessarily re-evaluating."""


def _run_agent(client: Any, model: str, messages: list[dict[str, Any]]) -> str:
	"""Run Grok tool calls to completion, preserving tool-call context in history."""
	for _ in range(6):
		response = client.chat.completions.create(
			model=model,
			messages=messages,
			tools=TOOLS,
			tool_choice="auto",
			temperature=0.3,
		)
		message = response.choices[0].message
		if not message.tool_calls:
			text = message.content or "I couldn't generate feedback. Please try again."
			messages.append({"role": "assistant", "content": text})
			return text

		assistant_entry: dict[str, Any] = {"role": "assistant", "content": message.content or ""}
		assistant_entry["tool_calls"] = [
			{
				"id": call.id,
				"type": "function",
				"function": {"name": call.function.name, "arguments": call.function.arguments},
			}
			for call in message.tool_calls
		]
		messages.append(assistant_entry)
		for call in message.tool_calls:
			name = call.function.name
			try:
				arguments = json.loads(call.function.arguments or "{}")
				result = TOOL_FUNCTIONS[name](**arguments)
			except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
				result = {"error": f"Tool could not run: {error}"}
			messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
	raise RuntimeError("Grok exceeded the tool-call limit. Please try again.")


def main() -> None:
	import streamlit as st
	from openai import OpenAI

	st.set_page_config(page_title="InterviewIQ", page_icon="🎤", layout="centered")
	st.title("🎤 InterviewIQ")
	st.caption("A supportive first-pass coach for interview answers")

	with st.sidebar:
		st.header("Grok setup")
		st.caption("Get an API key from xAI, then set GROK_API_KEY or enter it below.")
		api_key = st.text_input("Grok API key", value=os.getenv("GROK_API_KEY", ""), type="password")
		model = st.text_input("Model", value=os.getenv("GROK_MODEL", "grok-3-mini"))
		st.caption("API endpoint: https://api.x.ai/v1")
		if st.button("Clear session", use_container_width=True):
			st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
			st.session_state.transcript = []
			st.rerun()

	if "messages" not in st.session_state:
		st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
	if "transcript" not in st.session_state:
		st.session_state.transcript = []

	st.subheader("Evaluate an answer")
	with st.form("evaluation_form", clear_on_submit=True):
		question = st.text_input("Interview question", placeholder="Tell me about a time you handled a challenge.")
		answer = st.text_area("Candidate's spoken answer", height=150, placeholder="Enter or transcribe the candidate's answer...")
		evaluate = st.form_submit_button("Evaluate answer", type="primary")

	if evaluate:
		if not api_key:
			st.error("Add a Grok API key in the sidebar or set GROK_API_KEY.")
		elif not question.strip() or not answer.strip():
			st.warning("Enter both an interview question and an answer.")
		else:
			prompt = f"Evaluate this interview response.\n\nQuestion: {question.strip()}\n\nCandidate answer: {answer.strip()}"
			st.session_state.messages.append({"role": "user", "content": prompt})
			st.session_state.transcript.append({"role": "user", "content": f"**Question:** {question.strip()}\n\n**Answer:** {answer.strip()}"})
			try:
				client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
				with st.spinner("Reviewing the answer..."):
					feedback = _run_agent(client, model, st.session_state.messages)
				st.session_state.transcript.append({"role": "assistant", "content": feedback})
			except Exception as error:
				st.error(f"Grok request failed: {error}")
				st.session_state.messages.pop()

	st.subheader("Session coach")
	for item in st.session_state.transcript:
		with st.chat_message(item["role"]):
			st.markdown(item["content"])

	question_text = st.chat_input("Ask about this session or request another coaching tip...")
	if question_text:
		if not api_key:
			st.error("Add a Grok API key in the sidebar or set GROK_API_KEY.")
		else:
			st.session_state.messages.append({"role": "user", "content": question_text})
			st.session_state.transcript.append({"role": "user", "content": question_text})
			try:
				client = OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")
				with st.spinner("Thinking..."):
					reply = _run_agent(client, model, st.session_state.messages)
				st.session_state.transcript.append({"role": "assistant", "content": reply})
			except Exception as error:
				st.error(f"Grok request failed: {error}")
				st.session_state.messages.pop()
		st.rerun()


if __name__ == "__main__":
	main()
