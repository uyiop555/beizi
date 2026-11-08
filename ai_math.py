import os
from openai import AsyncOpenAI

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "sk-510aa156a1e9455797f5d7a32fa80db9")
client = AsyncOpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")

async def ask_math_ai(question: str):
    try:
        response = await client.chat.completions.create( #type: ignore
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个严谨的数学辅导老师。请一步步清晰地解答用户的数学问题。**非常重要**：所有数学公式必须使用标准的LaTeX语法，且仅使用Flet Markdown支持的格式。用课本上的方法展示运算符号，保持简洁通用，高中生可以看懂"},
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