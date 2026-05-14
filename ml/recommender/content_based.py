"""
Content-Based Recommender
Uses TF-IDF vectorization + Cosine Similarity to find similar books.

Formula:
    TF-IDF(t, d) = TF(t, d) × log(N / DF(t))
    Cosine Similarity = (A · B) / (‖A‖ × ‖B‖)
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DATASET_PATH = os.path.join(os.path.dirname(__file__), "../datasets/books.csv")
CACHE_PATH = os.path.join(os.path.dirname(__file__), "models/tfidf_cache.pkl")


class ContentBasedRecommender:
    def __init__(self):
        self.df = None
        self.tfidf_matrix = None
        self.vectorizer = None
        self._load_or_build()

    def _load_or_build(self):
        """Load cached TF-IDF matrix or build from dataset."""
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "rb") as f:
                cache = pickle.load(f)
                self.df = cache["df"]
                self.tfidf_matrix = cache["tfidf_matrix"]
                self.vectorizer = cache["vectorizer"]
            print("✅ ContentBasedRecommender: loaded from cache")
        elif os.path.exists(DATASET_PATH):
            self._build_from_dataset()
        else:
            print("⚠️  Dataset not found. Using demo mode.")
            self._build_demo()

    def _build_from_dataset(self):
        """Build TF-IDF matrix from Goodreads dataset."""
        self.df = pd.read_csv(DATASET_PATH, on_bad_lines="skip")
        # Combine title + authors + genres into a single feature string
        self.df["features"] = (
            self.df.get("title", "").fillna("") + " " +
            self.df.get("authors", "").fillna("") + " " +
            self.df.get("categories", self.df.get("genre", "")).fillna("")
        )
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=10000)
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["features"])
        self._save_cache()
        print(f"✅ ContentBasedRecommender: built from {len(self.df)} books")

    def _build_demo(self):
        """Demo data for development without the full dataset."""
        demo_data = [
            {"title": "Atomic Habits", "authors": "James Clear", "genre": "Self-Help", "rating": 4.37},
            {"title": "The Psychology of Money", "authors": "Morgan Housel", "genre": "Finance", "rating": 4.31},
            {"title": "Sapiens", "authors": "Yuval Noah Harari", "genre": "History", "rating": 4.40},
            {"title": "Deep Work", "authors": "Cal Newport", "genre": "Self-Help", "rating": 4.17},
            {"title": "The Alchemist", "authors": "Paulo Coelho", "genre": "Fiction", "rating": 3.88},
            {"title": "Thinking, Fast and Slow", "authors": "Daniel Kahneman", "genre": "Psychology", "rating": 4.18},
            {"title": "1984", "authors": "George Orwell", "genre": "Dystopia", "rating": 4.19},
            {"title": "Dune", "authors": "Frank Herbert", "genre": "Science Fiction", "rating": 4.26},
            {"title": "The Lean Startup", "authors": "Eric Ries", "genre": "Business", "rating": 3.91},
            {"title": "Man's Search for Meaning", "authors": "Viktor Frankl", "genre": "Psychology", "rating": 4.37},
        ]
        self.df = pd.DataFrame(demo_data)
        self.df["features"] = self.df["title"] + " " + self.df["authors"] + " " + self.df["genre"]
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["features"])

    def _save_cache(self):
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "wb") as f:
            pickle.dump({
                "df": self.df,
                "tfidf_matrix": self.tfidf_matrix,
                "vectorizer": self.vectorizer,
            }, f)

    def recommend(self, titles: list, top_k: int = 10) -> list:
        """
        Given a list of book titles, return top_k similar books.
        
        Algorithm:
        1. Find each input title in the dataset
        2. Average their TF-IDF vectors
        3. Compute cosine similarity with all books
        4. Return top_k (excluding inputs)
        """
        # Find indices of input books
        title_lower = [t.lower() for t in titles]
        indices = self.df[self.df["title"].str.lower().isin(title_lower)].index.tolist()

        if not indices:
            # Fallback: vectorize the query directly
            query_vec = self.vectorizer.transform([" ".join(titles)])
            sim_scores = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        else:
            # Average the vectors of matched books
            input_vectors = self.tfidf_matrix[indices]
            avg_vector = np.asarray(input_vectors.mean(axis=0))
            sim_scores = cosine_similarity(avg_vector, self.tfidf_matrix)[0]

        # Sort by similarity
        sim_scores = list(enumerate(sim_scores))
        sim_scores.sort(key=lambda x: x[1], reverse=True)

        # Exclude input books
        results = []
        for idx, score in sim_scores:
            if self.df.iloc[idx]["title"].lower() not in title_lower:
                row = self.df.iloc[idx]
                results.append({
                    "title": row["title"],
                    "authors": row.get("authors", "Unknown"),
                    "genre": row.get("genre", row.get("categories", "Unknown")),
                    "rating": float(row.get("rating", row.get("average_rating", 0))),
                    "similarity_score": round(score, 3),
                })
            if len(results) >= top_k:
                break

        return results
