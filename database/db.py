import asyncpg
from os import getenv
from color.style import *

async def get_connection():
    try:
        conn = await asyncpg.connect(
            database=getenv('DB_NAME'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASS'),
            host=getenv('DB_HOST', 'localhost'),
            port=getenv('DB_PORT', 5432)
        )
        print(lgreen + 'Database connection successful ✓' + reset)
        return conn
    except Exception as err:
        print(lred + f'Connection database error: {err}' + reset)
        return None

async def init_tables():
    conn = await get_connection()
    if not conn:
        return
    try:
        await conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            full_name VARCHAR(255) NOT NULL,
            role VARCHAR(20) DEFAULT 'student',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS learning_materials (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            file_id VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS material_chunks (
            id SERIAL PRIMARY KEY,
            material_id INT REFERENCES learning_materials(id) ON DELETE CASCADE,
            chunk_index INT NOT NULL,
            content TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS topics (
            id SERIAL PRIMARY KEY,
            material_id INT REFERENCES learning_materials(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            topic_order INT NOT NULL,
            difficulty VARCHAR(50) DEFAULT 'medium',
            estimated_minutes INT DEFAULT 30
        );

        CREATE TABLE IF NOT EXISTS study_plans (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
            material_id INT REFERENCES learning_materials(id) ON DELETE CASCADE,
            goal TEXT NOT NULL,
            exam_date DATE NOT NULL,
            days_per_week INT NOT NULL,
            session_duration_min INT NOT NULL,
            preferred_time TIME,
            current_level VARCHAR(50),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS study_plan_days (
            id SERIAL PRIMARY KEY,
            plan_id INT REFERENCES study_plans(id) ON DELETE CASCADE,
            topic_id INT REFERENCES topics(id) ON DELETE CASCADE,
            scheduled_date DATE NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            completed_at TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS lesson_tasks (
            id SERIAL PRIMARY KEY,
            plan_day_id INT REFERENCES study_plan_days(id) ON DELETE CASCADE,
            task_type VARCHAR(50) NOT NULL,
            content TEXT NOT NULL,
            is_completed BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS quiz_questions (
            id SERIAL PRIMARY KEY,
            topic_id INT REFERENCES topics(id) ON DELETE CASCADE,
            question_text TEXT NOT NULL,
            options JSONB,
            correct_option INT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS quiz_attempts (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
            topic_id INT REFERENCES topics(id) ON DELETE CASCADE,
            score INT NOT NULL,
            total_questions INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS student_answers (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
            task_id INT REFERENCES lesson_tasks(id) ON DELETE CASCADE,
            answer_text TEXT NOT NULL,
            ai_feedback TEXT,
            score INT DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS lesson_summaries (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
            plan_day_id INT REFERENCES study_plan_days(id) ON DELETE CASCADE,
            summary_text TEXT NOT NULL,
            ai_evaluation TEXT
        );

        CREATE TABLE IF NOT EXISTS topic_progress (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
            topic_id INT REFERENCES topics(id) ON DELETE CASCADE,
            mastery_level INT DEFAULT 0,
            is_weak BOOLEAN DEFAULT FALSE
        );

        CREATE TABLE IF NOT EXISTS mock_exams (
            id SERIAL PRIMARY KEY,
            user_id BIGINT REFERENCES users(telegram_id) ON DELETE CASCADE,
            score INT NOT NULL,
            readiness_percentage INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        print(green + 'Tables created successfully ✓' + reset)
    except Exception as err:
        print(red + f'Tables created error: {err}' + reset)
    finally:
        await conn.close()