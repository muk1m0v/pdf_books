from datetime import date


def build_learning_plan(
    topics: list[dict],
    deadline: date | None,
    study_days: list[str],
) -> list[dict]:
    return [
        {
            "topic": topic.get("title", "Untitled topic"),
            "deadline": deadline,
            "study_days": study_days,
        }
        for topic in topics
    ]
