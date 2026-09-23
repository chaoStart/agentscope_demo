import requests


url = "http://localhost:8080/v1/chat/completions"

payload = {
    "model": "minicpm5-1b-claude-opus-fable5-thinking",
    "messages": [
        {
            "role": "user",
            "content": "你好，请介绍一下你自己。",
        }
    ],
    "max_tokens": 512,
    "temperature": 0.7,
    "stream": False,
}

try:
    response = requests.post(
        url,
        json=payload,
        timeout=600,
    )

    print("HTTP状态码：", response.status_code)
    print("原始响应：", response.text)

    response.raise_for_status()

    result = response.json()
    answer = result["choices"][0]["message"]["content"]

    print("\n模型回答：")
    print(answer)

except requests.ConnectionError:
    print("无法连接 LocalAI，请检查容器和 8080 端口。")
except requests.Timeout:
    print("请求超时。首次推理需要加载模型，可能耗时较长。")
except requests.HTTPError as exc:
    print("LocalAI 返回错误：", exc)