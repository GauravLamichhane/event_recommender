import sys
import os
# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import RecommendationRequest, RecommendationResponse
from recommendation_service import RecommendationService

app = FastAPI(
    title="Event Recommendation API", 
    version="1.0.0",
    description="TF-IDF based event recommendation system"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Will update this after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize recommendation service
recommendation_service = RecommendationService()

@app.get("/")
async def root():
    return {
        "message": "Event Recommendation API", 
        "version": "1.0.0",
        "description": "Get personalized event recommendations using TF-IDF and cosine similarity"
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get personalized event recommendations for a user."""
    try:
        recommendations = recommendation_service.get_user_recommendations(
            user_id=request.user_id,
            limit=request.limit
        )
        
        if not recommendations:
            return RecommendationResponse(
                user_id=request.user_id,
                recommended_events=[],
                message="No events found matching your interests"
            )
        
        # Create message with event names
        event_names = [event.title for event in recommendations]
        message = f"Recommended events: {', '.join(event_names)}"
        
        return RecommendationResponse(
            user_id=request.user_id,
            recommended_events=recommendations,
            message=message
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
