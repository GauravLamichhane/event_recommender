# Create debug_user.py
from database_operations import DatabaseOperations

def debug_user(user_id):
    print(f"DEBUGGING USER {user_id}")
    print("=" * 30)
    
    db = DatabaseOperations()
    
    # Check if user exists and has interests
    try:
        interests = db.get_user_interests(user_id)
        print(f"User {user_id} interests: {repr(interests)}")
        
        if interests:
            print(f"Interests type: {type(interests)}")
            print(f"Interests length: {len(str(interests))}")
        else:
            print("❌ User has no interests or user doesn't exist")
            
    except Exception as e:
        print(f"❌ Error getting user interests: {e}")
    
    # Check available events
    try:
        events = db.get_all_events()
        print(f"\nTotal events in database: {len(events)}")
        
        if events:
            print("Sample events:")
            for event in events[:3]:
                print(f"  - {event['title']} (Category: {event['category_name']})")
        else:
            print("❌ No events in database")
            
    except Exception as e:
        print(f"❌ Error getting events: {e}")

if __name__ == "__main__":
    debug_user(13)  # Test with your user ID
