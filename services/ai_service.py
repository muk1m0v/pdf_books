class AIService:
    def __init__(self, api_key: str | None) -> None:
        self.api_key = api_key

    async def analyze_text(self, text: str) -> list[dict]:
        if not self.api_key:
            return []
        raise NotImplementedError("Connect AI provider here")

    async def answer_question(self, question: str, context: str) -> str:
        if not self.api_key:
            return "AI_API_KEY is not configured."
        raise NotImplementedError("Connect AI provider here")
