def calculate_quiz_score(correct_answers: int, total_questions: int) -> float:
    if total_questions <= 0:
        return 0.0
    return round(correct_answers / total_questions * 100, 2)
