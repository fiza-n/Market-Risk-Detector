"""
Flask Configuration settings
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'market-risk-detector-secret')
    MONGODB_URI = os.environ.get('MONGODB_URI', '')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    PORT = int(os.environ.get('PORT', 5000))
