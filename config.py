import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')


class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'


class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
