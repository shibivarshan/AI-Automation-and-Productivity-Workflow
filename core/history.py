import os
import sqlite3
from datetime import datetime

# Store DB in user's home directory to bypass Windows Defender "Controlled Folder Access" in Documents
DB_DIR = os.path.join(os.path.expanduser('~'), '.ai_workflow')
os.makedirs(DB_DIR, exist_ok=True)
DB_FILE = os.path.join(DB_DIR, "history.db")

def init_db():
    """Initializes the SQLite database and creates the table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            task_type TEXT,
            input_preview TEXT,
            output TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_task(task_type: str, input_data: str, output_data: str):
    """Logs a completed task to the database."""
    init_db()  # Ensure table exists
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    input_preview = input_data[:100] + "..." if len(input_data) > 100 else input_data
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO task_history (timestamp, task_type, input_preview, output)
            VALUES (?, ?, ?, ?)
        ''', (timestamp, task_type, input_preview, output_data))
        conn.commit()
        
        # Keep only the last 50 records
        cursor.execute('''
            DELETE FROM task_history WHERE id NOT IN (
                SELECT id FROM task_history ORDER BY id DESC LIMIT 50
            )
        ''')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error logging task to DB: {e}")

def get_history() -> list:
    """Retrieves the task history from the database."""
    init_db()
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('SELECT timestamp, task_type, input_preview, output FROM task_history ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        
        return [
            {
                "timestamp": row[0],
                "task_type": row[1],
                "input_preview": row[2],
                "output": row[3]
            }
            for row in rows
        ]
    except Exception as e:
        print(f"Error retrieving history: {e}")
        return []

def clear_history():
    """Clears the task history from the database."""
    init_db()
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM task_history')
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Error clearing history: {e}")
