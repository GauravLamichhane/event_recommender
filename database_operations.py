
from database import get_db_connection
from typing import List, Dict, Optional

# Rest of your DatabaseOperations class...

class DatabaseOperations:
    
    @staticmethod
    def get_user_interests(user_id: int) -> Optional[str]:
        """Get user interests as a single string."""
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT interests FROM users WHERE id = %s", (user_id,))  # Changed to 'interests'
            result = cur.fetchone()
            return result[0] if result else None
    
    @staticmethod
    def get_all_events() -> List[Dict]:
        """Get all events with their categories."""
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, description, category as category_name
                FROM events
            """)
            columns = [desc[0] for desc in cur.description]
            events = []
            for row in cur.fetchall():
                events.append(dict(zip(columns, row)))
            return events
    
    @staticmethod
    def get_events_by_category(category_name: str) -> List[Dict]:
        """Get events filtered by category."""
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, title, description, category as category_name
                FROM events
                WHERE category = %s
            """, (category_name,))
            columns = [desc[0] for desc in cur.description]
            events = []
            for row in cur.fetchall():
                events.append(dict(zip(columns, row)))
            return events
    
    @staticmethod
    def create_event(title: str, description: str, category_name: str) -> int:
        """Create a new event and return its ID."""
        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO events (title, description, category)
                VALUES (%s, %s, %s) RETURNING id
            """, (title, description, category_name))
            event_id = cur.fetchone()[0]
            conn.commit()
            return event_id
