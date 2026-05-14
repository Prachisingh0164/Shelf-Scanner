"""
Mood Classifier
Maps user mood → book recommendations using BERT embeddings + Logistic Regression.
"""

from typing import List

# Mood-to-genre/keyword mappings (used as fallback without BERT)
MOOD_PROFILES = {
    "happy": {
        "keywords": ["joy", "comedy", "humor", "uplifting", "light", "funny", "inspiring", "feel-good"],
        "genres": ["Comedy", "Romance", "Children", "Humor"],
    },
    "dark": {
        "keywords": ["dark", "dystopia", "thriller", "crime", "noir", "suspense", "psychological", "horror"],
        "genres": ["Dystopia", "Thriller", "Horror", "Crime"],
    },
    "motivational": {
        "keywords": ["success", "habits", "productivity", "growth", "mindset", "leadership", "entrepreneurship"],
        "genres": ["Self-Help", "Business", "Biography", "Motivational"],
    },
    "scifi": {
        "keywords": ["space", "future", "technology", "alien", "cyberpunk", "robot", "AI", "galaxy"],
        "genres": ["Science Fiction", "Sci-Fi", "Space Opera"],
    },
    "emotional": {
        "keywords": ["love", "loss", "grief", "family", "relationship", "emotional", "heartfelt", "moving"],
        "genres": ["Literary Fiction", "Drama", "Romance", "Family"],
    },
}

# Demo books per mood
MOOD_BOOKS = {
    "happy": [
        {"title": "The Hitchhiker's Guide to the Galaxy", "authors": "Douglas Adams", "rating": 4.22},
        {"title": "Good Omens", "authors": "Terry Pratchett & Neil Gaiman", "rating": 4.27},
        {"title": "A Man Called Ove", "authors": "Fredrik Backman", "rating": 4.35},
    ],
    "dark": [
        {"title": "1984", "authors": "George Orwell", "rating": 4.19},
        {"title": "Crime and Punishment", "authors": "Fyodor Dostoevsky", "rating": 4.25},
        {"title": "American Psycho", "authors": "Bret Easton Ellis", "rating": 3.97},
    ],
    "motivational": [
        {"title": "Atomic Habits", "authors": "James Clear", "rating": 4.37},
        {"title": "Can't Hurt Me", "authors": "David Goggins", "rating": 4.46},
        {"title": "The 7 Habits of Highly Effective People", "authors": "Stephen Covey", "rating": 4.14},
    ],
    "scifi": [
        {"title": "Dune", "authors": "Frank Herbert", "rating": 4.26},
        {"title": "Foundation", "authors": "Isaac Asimov", "rating": 4.19},
        {"title": "Neuromancer", "authors": "William Gibson", "rating": 3.88},
    ],
    "emotional": [
        {"title": "The Kite Runner", "authors": "Khaled Hosseini", "rating": 4.30},
        {"title": "A Little Life", "authors": "Hanya Yanagihara", "rating": 4.34},
        {"title": "The Fault in Our Stars", "authors": "John Green", "rating": 4.08},
    ],
}


class MoodClassifier:
    def __init__(self):
        # In production: load BERT model for mood classification
        # self.model = pipeline("text-classification", model="...")
        pass

    def classify_mood(self, text: str) -> str:
        """
        Classify the mood of a text description.
        In production: uses BERT classifier.
        Here: simple keyword matching.
        """
        text_lower = text.lower()
        scores = {}
        for mood, profile in MOOD_PROFILES.items():
            score = sum(1 for kw in profile["keywords"] if kw in text_lower)
            scores[mood] = score
        return max(scores, key=scores.get) if any(scores.values()) else "motivational"

    def filter_by_mood(self, books: List[dict], mood: str) -> List[dict]:
        """
        Filter a list of books by mood relevance.
        Uses genre/keyword matching.
        """
        if mood not in MOOD_PROFILES:
            return books
        target_genres = [g.lower() for g in MOOD_PROFILES[mood]["genres"]]
        filtered = [
            b for b in books
            if any(g in b.get("genre", "").lower() for g in target_genres)
        ]
        return filtered if filtered else books  # fallback: return all

    def recommend_by_mood(self, mood: str, top_k: int = 10) -> List[dict]:
        """Return books specifically curated for a mood."""
        books = MOOD_BOOKS.get(mood, MOOD_BOOKS["motivational"])
        return books[:top_k]
