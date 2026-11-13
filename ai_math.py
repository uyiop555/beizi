import os
import json
import httpx
from openai import AsyncOpenAI

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-510aa156a1e9455797f5d7a32fa80db9")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6KYAq1F11HYcVETHVmuzVLUrK401NWDvOUEG9iFP70ApA")

deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

SYSTEM_PROMPT = "若遇到数学问题，所有数学公式必须使用标准的LaTeX语法，且仅使用Flet Markdown支持的格式。用课本上的方法展示运算符号，保持简洁通用，高中生可以看懂"

async def get_ai_response(question: str, model_id: str):
    if model_id == "deepseek-flash":
        try:
            response = await deepseek_client.chat.completions.create( # type: ignore
                model="deepseek-flash",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                stream=True,
                temperature=0.3,
            )
            async for chunk in response:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
        except Exception as e:
            yield f"DeepSeek 请求出错：{e}"

    elif model_id == "gemini-4-hydrogen":
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:streamGenerateContent?alt=sse"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{SYSTEM_PROMPT}\n\n{question}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0.3
            }
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            try:
                                data_json = json.loads(data_str)
                                text_chunk = data_json["candidates"][0]["content"]["parts"][0]["text"]
                                if text_chunk:
                                    yield text_chunk
                            except (KeyError, IndexError, json.JSONDecodeError):
                                continue
        except Exception as e:
            yield f"Gemini 请求出错：{e}"
    else:
        yield "未知的模型"