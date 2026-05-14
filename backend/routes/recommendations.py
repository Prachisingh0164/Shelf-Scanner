"""
Recommendations Route — /api/recommend
Content-based, collaborative, and mood-based recommendations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../ml"))
from recommender.content_based import ContentBasedRecommender
from recommender.knn_recommender import KNNRecommender
from nlp.mood_classifier import MoodClassifier

router = APIRouter()

# Initialize models once
content_rec = ContentBasedRecommender()
knn_rec = KNNRecommender()
mood_clf = MoodClassifier()


class RecommendRequest(BaseModel):
    titles: List[str]
    mood: Optional[str] = None      # happy, dark, motivational, scifi, emotional
    top_k: Optional[int] = 10


class MoodRequest(BaseModel):
    mood: str                        # happy, dark, motivational, scifi, emotional
    top_k: Optional[int] = 10


@router.post("/")
async def get_recommendations(req: RecommendRequest):
    """
    Get book recommendations based on a list of book titles.
    Optionally filter by mood.
    """
    if not req.titles:
        raise HTTPException(status_code=400, detail="At least one book title required.")

    try:
        # Content-based recommendations
        content_results = content_rec.recommend(req.titles, top_k=req.top_k)

        # KNN recommendations
        knn_results = knn_rec.recommend(req.titles[0], top_k=5)

        # Merge and deduplicate
        seen = set()
        merged = []
        for book in content_results + knn_results:
            if book["title"] not in seen:
                seen.add(book["title"])
                merged.append(book)

        # Apply mood filter if provided
        if req.mood:
            merged = mood_clf.filter_by_mood(merged, req.mood)

        return {
            "success": True,
            "input_books": req.titles,
            "recommendations": merged[: req.top_k],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mood")
async def mood_recommendations(req: MoodRequest):
    """
    Get book recommendations based purely on mood.
    """
    valid_moods = ["happy", "dark", "motivational", "scifi", "emotional"]
    if req.mood.lower() not in valid_moods:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mood. Choose from: {', '.join(valid_moods)}",
        )

    try:
        results = mood_clf.recommend_by_mood(req.mood.lower(), top_k=req.top_k)
        return {"success": True, "mood": req.mood, "recommendations": results}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trending")
async def trending_books():
    """Return currently trending books (by rating/popularity)."""
    # Placeholder — in production, query your DB
    return {
        "success": True,
        "trending": [
            {"title": "Atomic Habits", "author": "James Clear", "rating": 4.37},
            {"title": "The Psychology of Money", "author": "Morgan Housel", "rating": 4.31},
            {"title": "Sapiens", "author": "Yuval Noah Harari", "rating": 4.40},
            {"title": "Deep Work", "author": "Cal Newport", "rating": 4.17},
            {"title": "The Alchemist", "author": "Paulo Coelho", "rating": 3.88},
        ],
    }
