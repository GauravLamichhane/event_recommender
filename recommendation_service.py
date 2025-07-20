

from database_operations import DatabaseOperations
from recommendation_engine import TFIDFRecommendationEngine
from models import EventResponse
from typing import List, Optional

class RecommendationService:
    def __init__(self):
        self.engine = TFIDFRecommendationEngine()
        self.db = DatabaseOperations()
        self.is_model_fitted = False
        self._fit_model()
    
    def _fit_model(self):
        try:
            events = self.db.get_all_events()
            if not events:
                return
            
            documents = []
            for event in events:
                title = str(event.get('title', '')).lower()
                description = str(event.get('description', '')).lower()
                category = str(event.get('category_name', '')).lower()
                doc = f"{title} {description} {category}".strip()
                if doc:
                    documents.append(doc)
            
            if documents:
                self.engine.fit(documents)
                self.is_model_fitted = True
                
        except Exception:
            pass
    
    def _process_user_interests(self, raw_interests) -> Optional[str]:
        if not raw_interests:
            return None
            
        try:
            if isinstance(raw_interests, list):
                processed = ' '.join(str(interest) for interest in raw_interests).lower()
            else:
                processed = str(raw_interests).lower()
            return processed.strip() if processed.strip() else None
        except Exception:
            return None
    
    def get_user_recommendations(self, user_id: int, limit: int = 10) -> List[EventResponse]:
        if not self.is_model_fitted:
            self._fit_model()
            if not self.is_model_fitted:
                return []
        
        try:
            raw_interests = self.db.get_user_interests(user_id)
            user_interests = self._process_user_interests(raw_interests)
            
            if not user_interests:
                return []
            
            events = self.db.get_all_events()
            if not events:
                return []
            
            event_documents = []
            event_ids = []
            
            for event in events:
                title = str(event.get('title', '')).lower()
                description = str(event.get('description', '')).lower() 
                category = str(event.get('category_name', '')).lower()
                doc = f"{title} {description} {category}".strip()
                if doc:
                    event_documents.append(doc)
                    event_ids.append(event['id'])
            
            if not event_documents:
                return []
            
            recommendations = self.engine.get_recommendations(
                user_profile=user_interests,
                event_documents=event_documents,
                event_ids=event_ids,
                limit=limit
            )
            
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
            
            return result
            
        except Exception:
            return []
    
    def refresh_model(self):
        self.is_model_fitted = False
        self._fit_model()
        
    def get_model_stats(self) -> dict:
        try:
            events = self.db.get_all_events()
            return {
                "is_fitted": self.is_model_fitted,
                "total_events": len(events) if events else 0,
                "vocabulary_size": len(self.engine.vocabulary) if hasattr(self.engine, 'vocabulary') else 0
            }
        except Exception as e:
            return {"is_fitted": self.is_model_fitted, "error": str(e)}
