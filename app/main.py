"""
Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.modules.image_converter import router as image_router
from app.modules.database import router as database_router, close_database_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager
    Xử lý startup và shutdown events
    """
    # Startup
    print("🚀 Starting Mirai Puzzle API...")
    print(f"📦 Version: {settings.app_version}")
    print(f"🗄️  MongoDB: {settings.mongodb_uri}")
    print(f"💾 Database: {settings.mongodb_database}")

    yield

    # Shutdown
    print("🛑 Shutting down...")
    await close_database_connection()
    print("✅ Database connection closed")


# Tạo FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API cho Mirai Puzzle - Image Converter & Database Management",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(image_router)
app.include_router(database_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "image_converter": "/image",
            "database": "/db",
            "docs": "/docs",
            "health": "/healthz",
        },
    }


@app.get("/healthz")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)
