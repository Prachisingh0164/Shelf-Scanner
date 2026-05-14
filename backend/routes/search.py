"""
Search Route — /api/search
Natural language semantic search using Sentence Transformers
"""

from fastapi import APIRouter, Query, HTTPException
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../ml"))
from nlp.semantic_search import SemanticSearch

router = APIRouter()
searcher = SemanticSearch()


@router.get("/")
async def search_books(
    q: str = Query(..., description="Search query (natural language)"),
    top_k: int = Query(10, ge=1, le=50),
):
    """
    Semantic book search.
    Example queries:
    - "books like Atomic Habits but darker"
    - "fantasy novels with strong female leads"
    - "motivational books for entrepreneurs"
    """
    if not q.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    try:
        results = searcher.search(q, top_k=top_k)
        return {
            "success": True,
            "query": q,
            "results": results,
            "count": len(results),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
