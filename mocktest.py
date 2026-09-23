from openai import OpenAI

client = OpenAI(
    api_key="localai",
    base_url="http://localhost:8080/v1",
    timeout=600,
    max_retries=0,
)

response = client.chat.completions.create(
    model="minicpm5-1b-claude-opus-fable5-thinking",
    messages=[
        {
            "role": "user",
            "content": "你好，请回复连接成功。",
        }
    ],
    max_tokens=64,
    temperature=0.1,
    stream=True,
)

for chunk in response:
    if not chunk.choices:
        continue

    delta = chunk.choices[0].delta

    reasoning = getattr(delta, "reasoning", None)
    if reasoning:
        print(f"[思考]{reasoning}", end="", flush=True)

    content = getattr(delta, "content", None)
    if content:
        print(content, end="", flush=True)

print()