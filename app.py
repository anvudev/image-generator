"""
Backward compatibility wrapper for v1.0 command
Allows running: uvicorn app:app --reload

This file imports the new modular app from app.main
For new development, use: uvicorn app.main:app --reload
"""

from app.main import app

__all__ = ["app"]
