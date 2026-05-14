"""
Dataset Downloader
Downloads the Goodreads books dataset from Kaggle.

Usage:
    pip install kaggle
    # Set up ~/.kaggle/kaggle.json with your API key
    python download_dataset.py
"""

import os
import sys

DATASET_DIR = os.path.dirname(__file__)


def download_from_kaggle():
    """Download Goodreads dataset from Kaggle."""
    try:
        import kaggle
        print("📥 Downloading Goodreads dataset from Kaggle...")
        kaggle.api.dataset_download_files(
            "jealousleopard/goodreadsbooks",
            path=DATASET_DIR,
            unzip=True,
        )
        print(f"✅ Dataset saved to {DATASET_DIR}/books.csv")
    except ImportError:
        print("❌ kaggle package not found. Install it: pip install kaggle")
        print("   Then set up your API key: https://www.kaggle.com/docs/api")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Download failed: {e}")
        print("\nManual download:")
        print("1. Go to: https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks")
        print("2. Download books.csv")
        print(f"3. Place it in: {DATASET_DIR}/")


def create_demo_dataset():
    """Create a small demo dataset for development."""
    import csv

    demo_books = [
        ["bookID", "title", "authors", "average_rating", "isbn", "language_code", "num_pages", "ratings_count", "text_reviews_count", "publication_date", "publisher"],
        [1, "Harry Potter and the Half-Blood Prince", "J.K. Rowling", 4.57, "0439785960", "eng", 652, 2095690, 27591, "9/16/2006", "Scholastic Inc."],
        [2, "Harry Potter and the Order of the Phoenix", "J.K. Rowling", 4.50, "0439358078", "eng", 870, 2153167, 29221, "9/1/2004", "Scholastic Inc."],
        [3, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling/Mary GrandPré", 4.47, "0439554934", "eng", 352, 5629932, 70390, "9/1/2003", "Scholastic Paperbacks"],
        [4, "Harry Potter and the Chamber of Secrets", "J.K. Rowling", 4.42, "0439554896", "eng", 352, 3436864, 36903, "11/1/2003", "Scholastic"],
        [5, "Harry Potter and the Prisoner of Azkaban", "J.K. Rowling/Mary GrandPré", 4.57, "043965548X", "eng", 435, 3748212, 41793, "5/1/2004", "Scholastic Inc."],
        [6, "The Hobbit or There and Back Again", "J.R.R. Tolkien", 4.27, "0618260307", "eng", 366, 2283914, 39477, "9/18/2007", "Mariner Books"],
        [7, "Atomic Habits", "James Clear", 4.37, "0735211299", "eng", 320, 1500000, 50000, "10/16/2018", "Avery"],
        [8, "Sapiens: A Brief History of Humankind", "Yuval Noah Harari", 4.40, "0062316095", "eng", 443, 1000000, 30000, "2/10/2015", "Harper"],
        [9, "1984", "George Orwell", 4.19, "0451524934", "eng", 328, 3500000, 60000, "7/1/1950", "Signet Classic"],
        [10, "Dune", "Frank Herbert", 4.26, "0441013597", "eng", 896, 1500000, 40000, "9/1/1965", "Ace"],
    ]

    demo_path = os.path.join(DATASET_DIR, "books_demo.csv")
    with open(demo_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(demo_books)

    print(f"✅ Demo dataset created: {demo_path}")
    print("   For full dataset, run: python download_dataset.py --full")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        create_demo_dataset()
    else:
        download_from_kaggle()
