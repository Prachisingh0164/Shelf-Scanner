# Datasets

## Goodreads Books Dataset

Download from: https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks

Expected filename: `books.csv`

### Columns used:
- `title` — book title
- `authors` — author name(s)
- `average_rating` — Goodreads average rating
- `language_code` — language
- `num_pages` — page count
- `ratings_count` — number of ratings

### Quick setup:
```bash
python download_dataset.py          # Full dataset (requires Kaggle API)
python download_dataset.py --demo   # Small demo dataset (no API needed)
```
