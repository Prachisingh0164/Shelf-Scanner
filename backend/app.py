"""
ShelfScanner - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from dotenv import load_dotenv

from routes.scanner import router as scanner_router
from routes.recommendations import router as recommendations_router
from routes.search import router as search_router
from routes.analytics import router as analytics_router

load_dotenv()

app = FastAPI(
    title="ShelfScanner API",
    description="AI-Powered Book Discovery — Scan shelves, get recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (uploaded images)
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Routers
app.include_router(scanner_router, prefix="/api/scan", tags=["Scanner"])
app.include_router(recommendations_router, prefix="/api/recommend", tags=["Recommendations"])
app.include_router(search_router, prefix="/api/search", tags=["Search"])
app.include_router(analytics_router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/")
async def root():
    return {
        "app": "ShelfScanner",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
