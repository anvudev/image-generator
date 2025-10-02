"""
Configuration file cho toàn bộ application
"""

try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for when pydantic-settings is not installed
    from pydantic import BaseSettings

from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    app_name: str = "Mirai Puzzle API"
    app_version: str = "2.0.0"
    debug: bool = True

    # CORS Settings
    cors_origins: list[str] = ["*"]

    # MongoDB Settings
    mongodb_uri: str = "mongodb://localhost:27017/"
    mongodb_database: str = "Mirai_Puzzle"

    # Image Converter Settings
    default_cols: int = 30
    default_rows: int = 30
    max_image_size: int = 10 * 1024 * 1024  # 10MB
    allowed_image_types: list[str] = ["image/png", "image/jpeg", "image/webp"]

    # Default Palette
    default_palette: dict[int, str] = {
        1: "#ff0000",  # Red
        2: "#0000ff",  # Blue
        3: "#00ff00",  # Green
        4: "#ffff00",  # Yellow
        5: "#ff9900",  # Orange
        6: "#9900ff",  # Purple
        7: "#ff00ff",  # Pink
        8: "#00ffff",  # Cyan
        9: "#4a86e8",  # Light Blue
        10: "#876670",  # Brown
        11: "#b7b7b7",  # Grey
        12: "#ffffff",  # White
    }

    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton instance
settings = Settings()
