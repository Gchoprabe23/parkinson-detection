#!/usr/bin/env python3
"""
config.py - Application Configuration Management
Handles environment-based configuration for different deployment stages
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./parkinsons.db")
    MODEL_PATH = os.getenv("MODEL_PATH", "model/parkinsons_detector.keras")
    BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
    
    # CORS settings
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    ALLOWED_ORIGINS = ["http://localhost:3000", "http://localhost:8501", "http://localhost:8000"]

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Must set ALLOWED_ORIGINS in .env for production
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = "sqlite:///./test.db"
    ALLOWED_ORIGINS = ["*"]

def get_config():
    """Get configuration based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionConfig()
    elif env == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()

# Export current configuration
config = get_config()
