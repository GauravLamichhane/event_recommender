

from database_operations import DatabaseOperations
from recommendation_engine import TFIDFRecommendationEngine
from models import EventResponse
from typing import List, Optional
import logging

# Rest of your RecommendationService class...

class RecommendationService:
    def __init__(self):
        self.engine = TFIDFRecommendationEngine()
        self.db = DatabaseOperations()
        self.is_model_fitted = False
        self._fit_model()
    
    def _fit_model(self):
        """Initialize and fit the TF-IDF model with all events."""
        try:
            events = self.db.get_all_events()
            if not events:
                logging.warning("No events found in database for model fitting")
                return
            
            # Combine title, description, and category for each event
            documents = []
            for event in events:
                # Ensure all fields are strings and handle None values
                title = str(event.get('title', '')).lower()
                description = str(event.get('description', '')).lower()
                category = str(event.get('category_name', '')).lower()
                
                doc = f"{title} {description} {category}".strip()
                if doc:  # Only add non-empty documents
                    documents.append(doc)
            
            if documents:
                # Fit the TF-IDF model
                self.engine.fit(documents)
                self.is_model_fitted = True
                print(f"✅ TF-IDF model fitted successfully with {len(documents)} events")
            else:
                print("❌ No valid documents found for model fitting")
                
        except Exception as e:
            print(f"❌ Error fitting model: {e}")
            logging.error(f"Model fitting error: {e}", exc_info=True)
    
    def _process_user_interests(self, raw_interests) -> Optional[str]:
        """Process user interests to handle different formats."""
        if not raw_interests:
            return None
            
        try:
            # Handle list format: ['Technology', 'Food', 'Adventure']
            if isinstance(raw_interests, list):
                processed = ' '.join(str(interest) for interest in raw_interests).lower()
            # Handle string format
            elif isinstance(raw_interests, str):
                processed = raw_interests.lower()
            else:
                processed = str(raw_interests).lower()
                
            return processed.strip() if processed.strip() else None
            
        except Exception as e:
            print(f"Error processing user interests: {e}")
            return None
    
    def get_user_recommendations(self, user_id: int, limit: int = 10) -> List[EventResponse]:
        """Get personalized event recommendations for a user."""
        if not self.is_model_fitted:
            print("⚠️  Model not fitted, attempting to fit model...")
            self._fit_model()
            if not self.is_model_fitted:
                return []
        
        try:
            # Get and process user interests
            raw_interests = self.db.get_user_interests(user_id)
            user_interests = self._process_user_interests(raw_interests)
            
            if not user_interests:
                print(f"❌ No valid interests found for user {user_id}")
                return []
            
            print(f"🔍 User {user_id} interests: '{user_interests}'")
            
            # Get all events
            events = self.db.get_all_events()
            if not events:
                print("❌ No events available for recommendations")
                return []
            
            # Prepare event documents and IDs
            event_documents = []
            event_ids = []
            
            for event in events:
                title = str(event.get('title', '')).lower()
                description = str(event.get('description', '')).lower() 
                category = str(event.get('category_name', '')).lower()
                
                doc = f"{title} {description} {category}".strip()
                if doc:  # Only include non-empty documents
                    event_documents.append(doc)
                    event_ids.append(event['id'])
            
            if not event_documents:
                print("❌ No valid event documents found")
                return []
            
            print(f"📊 Processing {len(event_documents)} events against user profile")
            
            # Get recommendations using TF-IDF engine
            recommendations = self.engine.get_recommendations(
                user_profile=user_interests,
                event_documents=event_documents,
                event_ids=event_ids,
                limit=limit
            )
            
            # Convert to response format
            result = []
            events_dict = {event['id']: event for event in events}
            
            for event_id, similarity_score in recommendations:
                if event_id in events_dict and similarity_score > 0:
                    event = events_dict[event_id]
                    result.append(EventResponse(
                        id=event['id'],
                        title=event['title'],
                        description=event['description'],
                        category_name=event['category_name'],
                        similarity_score=round(similarity_score, 4)
                    ))
            
            print(f"✅ Generated {len(result)} recommendations for user {user_id}")
            return result
            
        except Exception as e:
            print(f"❌ Error getting recommendations for user {user_id}: {e}")
            logging.error(f"Recommendation error for user {user_id}: {e}", exc_info=True)
            return []
    
    def refresh_model(self):
        """Refresh the TF-IDF model with updated events."""
        print("🔄 Refreshing recommendation model...")
        self.is_model_fitted = False
        self._fit_model()
        
    def get_model_stats(self) -> dict:
        """Get statistics about the current model."""
        try:
            events = self.db.get_all_events()
            return {
                "is_fitted": self.is_model_fitted,
                "total_events": len(events) if events else 0,
                "vocabulary_size": len(self.engine.vocabulary) if hasattr(self.engine, 'vocabulary') else 0
            }
        except Exception as e:
            return {
                "is_fitted": self.is_model_fitted,
                "error": str(e)
            }
