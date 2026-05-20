# 📚 ShelfScanner — AI-Powered Book Discovery App

<div align="center">

![ShelfScanner Banner](https://img.shields.io/badge/ShelfScanner-AI%20Book%20Discovery-6C63FF?style=for-the-badge&logo=bookstack&logoColor=white)

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Scan your bookshelf → AI detects books → Get personalized recommendations**
<img width="793" height="506" alt="Screenshot 2026-05-20 121522" src="https://github.com/user-attachments/assets/90dc0a52-86d9-4498-805b-355cfc5e0800" />


</div>

---

## 🎯 What is ShelfScanner?

ShelfScanner is an AI-powered web application that lets you **photograph any bookshelf** and instantly:
- 📖 Detects all books using YOLOv8 object detection
- 🔤 Extracts titles using EasyOCR
- 🤖 Recommends similar books via ML (TF-IDF, KNN, Collaborative Filtering)
- 😊 Suggests books based on your **current mood**
- 🔍 Supports **natural language search** ("books like Atomic Habits but darker")
- 📊 Tracks your reading analytics with a personalized dashboard

---

## ✨ Features

### 🔍 1. Bookshelf Scanner
Upload a photo of any bookshelf — ShelfScanner automatically:
- Detects book spines using **YOLOv8**
- Extracts text with **EasyOCR / Tesseract**
- Looks up book metadata from the Goodreads dataset

### 🤖 2. AI Recommendation Engine
- **TF-IDF + Cosine Similarity** for content-based filtering
- **KNN Recommender** for nearest-neighbor suggestions
- **Collaborative Filtering** for user-behavior-based picks

### 😊 3. Mood-Based Recommendations
Select your mood: Happy • Motivational • Dark • Sci-fi • Emotional
Uses **BERT embeddings** + **Sentiment Analysis** to match books to your vibe.

### 🔎 4. Smart Semantic Search
Natural language queries powered by **Sentence Transformers**:
> "Suggest books like Atomic Habits but darker"
> "Fantasy novels with strong female leads"

### 📊 5. Reading Analytics Dashboard
- Track scanned books over time
- Visualize favorite genres (K-Means clustering)
- Reading trend analysis

---

## 🏗️ Architecture

```
User Uploads Image
        ↓
YOLOv8 Detects Books (bounding boxes)
        ↓
EasyOCR Extracts Titles
        ↓
NLP Cleans & Normalizes Text
        ↓
Recommendation Engine (TF-IDF → Cosine Similarity)
        ↓
FastAPI serves results
        ↓
React Frontend displays recommendations
```

---

## 🧠 ML Algorithms Used

| Feature | Algorithm |
|---|---|
| Book Detection | YOLOv8 |
| OCR | EasyOCR + Tesseract |
| Recommendation | KNN + Collaborative Filtering |
| Text Similarity | TF-IDF + Cosine Similarity |
| Semantic Search | Sentence Transformers (all-MiniLM-L6-v2) |
| Mood Classification | Logistic Regression / BERT |
| Genre Clustering | K-Means |

---

## 🏗️ Tech Stack

### Frontend
- **React 18** + Vite
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **Axios** for API calls
- **Recharts** for analytics

### Backend
- **FastAPI** (Python 3.11+)
- **Uvicorn** ASGI server
- **Pydantic** for data validation

### ML & AI
- **YOLOv8** (Ultralytics) — object detection
- **EasyOCR** — optical character recognition
- **Scikit-learn** — TF-IDF, KNN, K-Means
- **Sentence Transformers** — semantic search
- **Hugging Face Transformers** — BERT for mood analysis
- **OpenCV** — image preprocessing

### Database
- **MongoDB Atlas** (production) / **SQLite** (development)

### Deployment
- **Vercel** — Frontend
- **Render / Railway** — Backend
- **Docker** — Containerization
- **MongoDB Atlas** — Cloud DB

---

## 📁 Project Structure

```
ShelfScanner/
│
├── 📂 frontend/                  # React frontend
│   ├── src/
│   │   ├── components/           # Reusable UI components
│   │   │   ├── BookCard.jsx
│   │   │   ├── BookShelfScanner.jsx
│   │   │   ├── MoodSelector.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   └── Navbar.jsx
│   │   ├── pages/                # Route pages
│   │   │   ├── Home.jsx
│   │   │   ├── Scanner.jsx
│   │   │   ├── Recommendations.jsx
│   │   │   ├── Search.jsx
│   │   │   └── Dashboard.jsx
│   │   ├── hooks/                # Custom React hooks
│   │   │   ├── useBookScanner.js
│   │   │   └── useRecommendations.js
│   │   └── utils/
│   │       └── api.js
│   ├── package.json
│   └── vite.config.js
│
├── 📂 backend/                   # FastAPI backend
│   ├── app.py                    # Main entry point
│   ├── routes/
│   │   ├── scanner.py            # /api/scan endpoint
│   │   ├── recommendations.py    # /api/recommend endpoint
│   │   ├── search.py             # /api/search endpoint
│   │   └── analytics.py         # /api/analytics endpoint
│   ├── models/
│   │   ├── book.py               # Pydantic models
│   │   └── user.py
│   └── utils/
│       ├── ocr.py                # EasyOCR wrapper
│       ├── preprocess.py         # Image preprocessing
│       └── db.py                 # Database connection
│
├── 📂 ml/                        # ML modules
│   ├── book_detector/
│   │   ├── detector.py           # YOLOv8 wrapper
│   │   └── train.py              # Custom training script
│   ├── recommender/
│   │   ├── content_based.py      # TF-IDF + Cosine Similarity
│   │   ├── collaborative.py      # Collaborative Filtering
│   │   └── knn_recommender.py    # KNN model
│   ├── nlp/
│   │   ├── mood_classifier.py    # BERT mood classification
│   │   ├── semantic_search.py    # Sentence Transformers
│   │   └── text_cleaner.py       # NLP preprocessing
│   └── datasets/
│       ├── download_dataset.py   # Dataset downloader
│       └── README.md
│
├── 📂 docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   └── nginx.conf
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ShelfScanner.git
cd ShelfScanner
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# Copy environment variables
cp ../.env.example .env
# Edit .env with your values

# Start the backend
uvicorn app:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Docker (Recommended)
```bash
# Start all services
docker-compose up --build

# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

---

## 📡 API Docs

Once running, visit: **http://localhost:8000/docs** (Swagger UI)

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/scan` | Upload bookshelf image, get detected books |
| `POST` | `/api/recommend` | Get book recommendations |
| `GET` | `/api/search?q=...` | Semantic book search |
| `POST` | `/api/mood` | Mood-based recommendations |
| `GET` | `/api/analytics/{user_id}` | Reading analytics |

### Example: Scan a Bookshelf
```bash
curl -X POST "http://localhost:8000/api/scan" \
  -H "Content-Type: multipart/form-data" \
  -F "image=@bookshelf.jpg"
```

**Response:**
```json
{
  "detected_books": [
    {"title": "Atomic Habits", "confidence": 0.94},
    {"title": "The Psychology of Money", "confidence": 0.89}
  ],
  "recommendations": [...]
}
```

---

## 📊 Dataset

Download the Goodreads dataset:
```bash
cd ml/datasets
python download_dataset.py
```

Or manually from [Kaggle - Goodreads Books Dataset](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks)

---

## ☁️ Deployment

### Frontend → Vercel
```bash
cd frontend
npm run build
npx vercel --prod
```

### Backend → Render
1. Connect your GitHub repo to [Render](https://render.com)
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
4. Add environment variables from `.env.example`

### Full Stack → Docker
```bash
docker-compose -f docker-compose.yml up -d
```

---

## 🤝 Contributing

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push: `git push origin feature/AmazingFeature`
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## 🙏 Acknowledgements

- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [Hugging Face Transformers](https://huggingface.co/transformers)
- [Goodreads Dataset on Kaggle](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks)
- [Scikit-learn](https://scikit-learn.org)

---

<div align="center">
Made with ❤️ by Prachi Singh
</div>
