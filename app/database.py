import sqlite3
from datetime import datetime
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "applications.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            job_title TEXT,
            sponsorship_category TEXT,
            h1b_history_rating TEXT,
            final_ats_score INTEGER,
            recommendation TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_application_analysis(
    company_name,
    job_title,
    sponsorship_category,
    h1b_history_rating,
    final_ats_score,
    recommendation
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications (
            company_name,
            job_title,
            sponsorship_category,
            h1b_history_rating,
            final_ats_score,
            recommendation,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        company_name,
        job_title,
        sponsorship_category,
        h1b_history_rating,
        final_ats_score,
        recommendation,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            company_name,
            job_title,
            sponsorship_category,
            h1b_history_rating,
            final_ats_score,
            recommendation,
            created_at
        FROM applications
        ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows