"""
KNN Recommender
K-Nearest Neighbors for book recommendation based on feature vectors.
"""

import os
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_extraction.text import TfidfVectorizer


DATASET_PATH = os.path.join(os.path.dirname(__file__), "../datasets/books.csv")


class KNNRecommender:
    def __init__(self, n_neighbors: int = 6):
        self.n_neighbors = n_neighbors
        self.model = NearestNeighbors(n_neighbors=n_neighbors, metric="cosine", algorithm="brute")
        self.df = None
        self.matrix = None
        self._load()

    def _load(self):
        if os.path.exists(DATASET_PATH):
            self.df = pd.read_csv(DATASET_PATH, on_bad_lines="skip")
            self.df["features"] = (
                self.df.get("title", "").fillna("") + " " +
                self.df.get("authors", "").fillna("")
            )
        else:
            # Demo data
            self.df = pd.DataFrame([
                {"title": "Atomic Habits", "authors": "James Clear", "rating": 4.37},
                {"title": "Deep Work", "authors": "Cal Newport", "rating": 4.17},
                {"title": "The Psychology of Money", "authors": "Morgan Housel", "rating": 4.31},
                {"title": "Sapiens", "authors": "Yuval Noah Harari", "rating": 4.40},
                {"title": "Thinking, Fast and Slow", "authors": "Daniel Kahneman", "rating": 4.18},
            ])
            self.df["features"] = self.df["title"] + " " + self.df["authors"]

        vec = TfidfVectorizer(stop_words="english")
        self.matrix = vec.fit_transform(self.df["features"])
        self.model.fit(self.matrix)

    def recommend(self, title: str, top_k: int = 5) -> list:
        """Find KNN for a given book title."""
        matches = self.df[self.df["title"].str.lower() == title.lower()]
        if matches.empty:
            return []

        idx = matches.index[0]
        distances, indices = self.model.kneighbors(self.matrix[idx])

        results = []
        for i, dist in zip(indices[0], distances[0]):
            if i == idx:
                continue
            row = self.df.iloc[i]
            results.append({
                "title": row["title"],
                "authors": row.get("authors", "Unknown"),
                "rating": float(row.get("rating", row.get("average_rating", 0))),
                "knn_distance": round(float(dist), 3),
            })
        return results[:top_k]
