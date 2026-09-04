import aiohttp
from config import GEMINI_API_KEY

MODEL = "gemini-3.6-flash"
API_URL = "https://generativelanguage.googleapis.com/v1beta2/interactions"

MAX_CONTEXT_CHARS = 25000


def _extract_text(data: dict) -> str | None:
    """Достаёт текст ответа модели из структуры Interactions API."""
    # На случай если появится удобное поле верхнего уровня
    if data.get("output_text"):
        return data["output_text"]

    parts = []
    for step in data.get("steps", []):
        if step.get("type") == "model_output":
            for block in step.get("content", []):
                if block.get("type") == "text" and block.get("text"):
                    parts.append(block["text"])

    return "\n".join(parts) if parts else None


async def ask_about_book(question: str, book_title: str, book_text: str) -> str:
    context = book_text[:MAX_CONTEXT_CHARS]

    prompt = (
        f"Ты — помощник, который отвечает на вопросы по содержимому книги «{book_title}».\n"
        f"Отвечай только на основе текста ниже. Если ответа в тексте нет — так и скажи.\n\n"
        f"ТЕКСТ КНИГИ:\n{context}\n\n"
        f"ВОПРОС: {question}"
    )

    payload = {
        "model": MODEL,
        "input": prompt,
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
            data = await resp.json()

            if resp.status != 200:
                error_msg = data.get("error", {}).get("message", str(data))
                return f"Ошибка AI API ({resp.status}): {error_msg}"

            text = _extract_text(data)
            if text:
                return text

            return "Не удалось получить ответ от AI. Попробуй переформулировать вопрос."