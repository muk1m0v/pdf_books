import aiohttp
from config import GEMINI_API_KEY

MODEL = "gemini-3.6-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

MAX_CONTEXT_CHARS = 25000


async def ask_about_book(question: str, book_title: str, book_text: str) -> str:
    context = book_text[:MAX_CONTEXT_CHARS]

    prompt = (
        f"Ты — помощник, который отвечает на вопросы по содержимому книги «{book_title}».\n"
        f"Отвечай только на основе текста ниже. Если ответа в тексте нет — так и скажи.\n\n"
        f"ТЕКСТ КНИГИ:\n{context}\n\n"
        f"ВОПРОС: {question}"
    )

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            API_URL,
            json=payload,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as resp:
            raw = await resp.text()

            if resp.status != 200:
                return f"Ошибка AI API ({resp.status}): {raw[:300]}"

            try:
                data = await resp.json(content_type=None)
            except Exception:
                return f"Не удалось разобрать ответ AI API. Сырой ответ: {raw[:300]}"

            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError, TypeError):
                return "Не удалось получить ответ от AI. Попробуй переформулировать вопрос."