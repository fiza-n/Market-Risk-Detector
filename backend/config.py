"""
Flask Configuration settings
"""
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'market-risk-detector-secret')
    MONGO_URI = os.environ.get('MONGO_URI', '')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    PORT = int(os.environ.get('PORT', 5000))
