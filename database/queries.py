from database.db import get_connection

async def get_student_report(telegram_id: int):
    conn = await get_connection()
    if not conn:
        return None
    
    query = '''
        SELECT 
            u.full_name,
            COUNT(DISTINCT spd.id) FILTER (WHERE spd.status = 'completed') AS completed_lessons,
            COUNT(DISTINCT spd.id) FILTER (WHERE spd.status = 'skipped') AS skipped_lessons,
            COALESCE(AVG(qa.score * 100.0 / NULLIF(qa.total_questions, 0)), 0) AS avg_quiz_score,
            COUNT(DISTINCT tp.id) FILTER (WHERE tp.is_weak = TRUE) AS weak_topics_count
        FROM users u
        LEFT JOIN study_plans sp ON u.telegram_id = sp.user_id
        LEFT JOIN study_plan_days spd ON sp.id = spd.plan_id
        LEFT JOIN quiz_attempts qa ON u.telegram_id = qa.user_id
        LEFT JOIN topic_progress tp ON u.telegram_id = tp.user_id
        WHERE u.telegram_id = $1
        GROUP BY u.telegram_id, u.full_name;
    '''
    
    row = await conn.fetchrow(query, telegram_id)
    await conn.close()
    return row