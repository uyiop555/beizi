import os
from openai import AsyncOpenAI

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-510aa156a1e9455797f5d7a32fa80db9")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6LZ8PBhw1kHx9iMLs9XqpC1SuJhTJknyt1bGyWw9F2TMA")

deepseek_client = AsyncOpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
gemini_client = AsyncOpenAI(api_key=GEMINI_API_KEY, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

SYSTEM_PROMPT = r"若遇到数学问题，所有数学公式必须使用标准的LaTeX语法。行内公式请使用 $...$，块级公式请使用 $$...$$。**不要**使用 \[ ... \] 或 \( ... \) 等非标准格式。**不要**使用 \cdot，请使用 \cdot 表示乘号。"

async def get_ai_response(question: str, model_id: str):
    if model_id == "deepseek-flash":
        client = deepseek_client
        actual_model = "deepseek-flash"
    elif model_id == "gemini-4-hydrogen":
        client = gemini_client
        actual_model = "gemini-4-hydrogen"
    else:
        yield "滚木"
        return

    try:
        response = await client.chat.completions.create(  # type: ignore
            model=actual_model,
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
        yield f"请求出错：{e}"