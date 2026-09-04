import aiohttp
from config import GEMINI_API_KEY

MODEL = "gemini-2.0-flash"
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
            {"parts": [{"text": prompt}]}
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{API_URL}?key={GEMINI_API_KEY}",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=60),
        ) as resp:
            data = await resp.json()

            if resp.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                return f"Ошибка AI API ({resp.status}): {error_msg}"

            try:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                return "Не удалось получить ответ от AI. Попробуй переформулировать вопрос."
