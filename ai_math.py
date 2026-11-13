import os
from openai import AsyncOpenAI
from google import genai

DEEPSEEK_API_KEY = "sk-510aa156a1e9455797f5d7a32fa80db9"
GEMINI_API_KEY = "AQ.Ab8RN6KYAq1F11HYcVETHVmuzVLUrK401NWDvOUEG9iFP70ApA"

deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = "平时正常回答，若遇到数学问题，所有数学公式必须使用标准的LaTeX语法，且仅使用Flet Markdown支持的格式。用课本上的方法展示运算符号，保持简洁通用，高中生可以看懂。"

async def get_ai_response(question: str, model_id: str):
    if model_id == "deepseek-flash":
        try:
            response = await deepseek_client.chat.completions.create( #type: ignore
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
        try:
            response = await gemini_client.aio.models.generate_content_stream(
                model="gemini-flash-latest",
                contents=f"{SYSTEM_PROMPT}\n\n{question}",
            )
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Gemini 请求出错：{e}"
    else:
        yield "未知的模型"