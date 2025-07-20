
from database import get_db_connection
from typing import List, Dict, Optional

class DatabaseOperations:
    
    @staticmethod
    def get_user_interests(user_id: int) -> Optional[str]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT interests FROM users WHERE id = %s", (user_id,))
            result = cur.fetchone()
            return result[0] if result else None
    
    @staticmethod
    def get_all_events() -> List[Dict]:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, title, description, category as category_name FROM events")
            columns = [desc[0] for desc in cur.description]
            return [dict(zip(columns, row)) for row in cur.fetchall()]
    
    @staticmethod
    def create_event(title: str, description: str, category_name: str) -> int:
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO events (title, description, category)
                VALUES (%s, %s, %s) RETURNING id
            """, (title, description, category_name))
            event_id = cur.fetchone()[0]
            conn.commit()
            return event_id
