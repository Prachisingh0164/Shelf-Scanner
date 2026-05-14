"""
Semantic Search
Uses Sentence Transformers (all-MiniLM-L6-v2) for natural language book search.
"""

import os
import numpy as np
import pandas as pd


DATASET_PATH = os.path.join(os.path.dirname(__file__), "../datasets/books.csv")
MODEL_NAME = "all-MiniLM-L6-v2"


class SemanticSearch:
    def __init__(self):
        self.model = None
        self.embeddings = None
        self.df = None
        self._load()

    def _load(self):
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(MODEL_NAME)
            print(f"✅ SemanticSearch: loaded {MODEL_NAME}")
        except ImportError:
            print("⚠️  sentence-transformers not installed.")

        # Load dataset
        if os.path.exists(DATASET_PATH):
            self.df = pd.read_csv(DATASET_PATH, on_bad_lines="skip")
        else:
            self._load_demo()

        # Build embeddings
        if self.model and self.df is not None:
            texts = (
                self.df.get("title", "").fillna("") + " by " +
                self.df.get("authors", "").fillna("") + ". " +
                self.df.get("description", self.df.get("genre", "")).fillna("")
            ).tolist()
            self.embeddings = self.model.encode(texts, show_progress_bar=True)
            print(f"✅ Built embeddings for {len(texts)} books")

    def _load_demo(self):
        self.df = pd.DataFrame([
            {"title": "Atomic Habits", "authors": "James Clear", "genre": "Self-Help", "rating": 4.37,
             "description": "A guide to building good habits and breaking bad ones"},
            {"title": "1984", "authors": "George Orwell", "genre": "Dystopia", "rating": 4.19,
             "description": "A dark dystopian novel about totalitarian surveillance state"},
            {"title": "Dune", "authors": "Frank Herbert", "genre": "Science Fiction", "rating": 4.26,
             "description": "An epic space opera set in the distant future on a desert planet"},
            {"title": "The Kite Runner", "authors": "Khaled Hosseini", "genre": "Literary Fiction", "rating": 4.30,
             "description": "An emotional story of friendship, guilt and redemption in Afghanistan"},
            {"title": "Sapiens", "authors": "Yuval Noah Harari", "genre": "History", "rating": 4.40,
             "description": "A brief history of humankind from ancient to modern times"},
        ])

    def search(self, query: str, top_k: int = 10) -> list:
        """
        Semantic search: encodes query, finds most similar books by cosine similarity.
        """
        if self.model is None or self.embeddings is None:
            return self._keyword_fallback(query, top_k)

        from sentence_transformers import util
        query_embedding = self.model.encode(query)
        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]
        top_indices = np.argsort(-cos_scores.numpy())[:top_k]

        results = []
        for idx in top_indices:
            row = self.df.iloc[int(idx)]
            results.append({
                "title": row["title"],
                "authors": row.get("authors", "Unknown"),
                "genre": row.get("genre", "Unknown"),
                "rating": float(row.get("rating", row.get("average_rating", 0))),
                "similarity": round(float(cos_scores[idx]), 3),
            })
        return results

    def _keyword_fallback(self, query: str, top_k: int) -> list:
        """Simple keyword search fallback when Sentence Transformers unavailable."""
        query_lower = query.lower()
        results = []
        for _, row in self.df.iterrows():
            text = f"{row.get('title', '')} {row.get('authors', '')} {row.get('genre', '')}".lower()
            if any(word in text for word in query_lower.split()):
                results.append({
                    "title": row["title"],
                    "authors": row.get("authors", "Unknown"),
                    "genre": row.get("genre", "Unknown"),
                    "rating": float(row.get("rating", 0)),
                    "similarity": 0.5,
                })
        return results[:top_k]
