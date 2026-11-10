# Shipment Exception Desk -- Starter Kit

## Setup
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then paste your GROQ_API_KEY inside
```
Get a free Groq key at https://console.groq.com

## What to do
Read `Problem_Statement_and_Milestones.md` (in the project root, one level
up) for the full problem statement and the asks. In short:
1. `tools.py` -- implement the three compensation calculators (each returns a dict).
2. `pipeline.py` -- this is the core exercise. Implement `process_exception`:
   call the chains from `chains.py`, branch on the category, decide whether
   to escalate, and call the right drafting chain.
3. `session.py` -- track every processed exception and build a Daily Triage
   Summary that names the costliest category, not just a flat recap.
4. Check your pipeline actually works:
```bash
python triage_check.py
```
5. `app.py` -- wrap it all in the (mandatory) Gradio interface.

This is your first LangChain project, so it's kept intentionally simple:
the LLM client, the three prompt chains, the CLI harness, and the test
harness (`main.py`, `triage_check.py`) are all given. The compensation
logic, the pipeline's branching, the aggregation, and the UI's event
handlers are yours to build.

## Files
| File | What it is |
|---|---|
| `llm.py` | Shared LangChain chat model (Groq by default). Given -- plumbing. |
| `chains.py` | Given -- three ready-made LangChain chains (classify / escalate / draft email), same `prompt \| model \| parser` pattern as Class 2. |
| `tools.py` | **Your task.** Three compensation calculators. |
| `pipeline.py` | **Your task, and the core exercise.** Wire the chains and the compensation functions together with plain Python control flow. |
| `session.py` | **Your task.** Daily Triage Log + costliest-category aggregation. |
| `app.py` | **Your task.** Gradio interface -- required, not optional. Layout is given; the handler functions are yours. |
| `main.py` | CLI runner. Given -- handy for quick terminal testing while you build. |
| `triage_check.py` | Given -- a scripted check that exercises all four category/escalation branches. Run it once Ask 1 is done. |
| `requirements.txt` | Python packages needed (`pip install -r requirements.txt`). |
| `.env.example` | Copy to `.env` and add your API key. Never commit the real `.env`. |
| `.gitignore` | Keeps your venv, `.env`, and cache files out of git. |
