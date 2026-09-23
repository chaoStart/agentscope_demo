import json
import sys

import requests


# 保证 Python 控制台使用 UTF-8。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

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
    "stream": True,
}

try:
    with requests.post(
        url,
        json=payload,
        stream=True,
        timeout=(10, 600),
    ) as response:
        print("HTTP状态码：", response.status_code)
        print("响应Content-Type：", response.headers.get("Content-Type"))
        print("requests推断编码：", response.encoding)

        if response.status_code != 200:
            # 错误响应也按 UTF-8 解析。
            response.encoding = "utf-8"
            print("错误响应：", response.text)
            response.raise_for_status()

        # 关键修改：强制使用 UTF-8。
        response.encoding = "utf-8"

        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue

            print("原始流数据：", line)

            if not line.startswith("data:"):
                continue

            data_text = line[len("data:"):].strip()

            if data_text == "[DONE]":
                print("\n流式输出结束")
                break

            try:
                event = json.loads(data_text)
            except json.JSONDecodeError as exc:
                print("JSON解析失败：", exc)
                print("异常数据：", data_text)
                continue

            choices = event.get("choices") or []
            if not choices:
                continue

            delta = choices[0].get("delta") or {}

            reasoning = (
                delta.get("reasoning")
                or delta.get("reasoning_content")
            )

            content = delta.get("content")

            if reasoning:
                print(
                    f"[思考]{reasoning}",
                    end="",
                    flush=True,
                )

            if content:
                print(
                    content,
                    end="",
                    flush=True,
                )

except requests.RequestException as exc:
    print("调用 LocalAI 失败：", exc)