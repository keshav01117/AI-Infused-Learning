def battle(prompt):
    msgs = [{"role": "user", "content": prompt}]

    # Model A — OpenAI's GPT
    a = openai_client.chat.completions.create(model="gpt-4o-mini", messages=msgs)

    # Model B — Llama on Groq (same code, different brain!)
    b = groq_client.chat.completions.create(model="llama-3.3-70b-versatile", messages=msgs)

    return a.choices[0].message.content, b.choices[0].message.content
# …now we wrap this in Gradio with two columns + thumbs up/down 👇