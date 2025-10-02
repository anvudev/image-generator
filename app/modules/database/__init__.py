"""
Database Module
Quản lý MongoDB operations
"""
from .routes import router
from .connection import get_database, close_database_connection

__all__ = ["router", "get_database", "close_database_connection"]

