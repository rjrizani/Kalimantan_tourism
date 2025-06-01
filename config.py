import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://username:password@localhost/kalimantan_tourism'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Articles API Configuration
    ARTICLES_API_URL = os.environ.get('ARTICLES_API_URL') or 
    API_KEY = os.environ.get('API_KEY') or 'your-api-key-here'  # Change this in production