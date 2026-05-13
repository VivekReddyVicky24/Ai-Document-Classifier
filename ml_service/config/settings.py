import os
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).parent

# Flask Configuration
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ENV = os.getenv('FLASK_ENV', 'development')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Server Configuration
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5001))
THREADED = os.getenv('THREADED', 'True').lower() == 'true'

# Model Configuration
EMBEDDING_MODEL_NAME = 'BAAI/bge-large-en-v1.5'
STACK_MODEL_PATH = os.getenv('STACK_MODEL_PATH', os.path.join(BASE_DIR, 'models', 'stack_model.pkl'))
LABEL_ENCODER_PATH = os.getenv('LABEL_ENCODER_PATH', os.path.join(BASE_DIR, 'models', 'label_encoder.pkl'))

# Device Configuration (GPU vs CPU)
DEVICE = os.getenv('DEVICE', 'cpu')  # Set to 'cuda' if GPU available

# File Upload Configuration
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
UPLOAD_DIR = os.getenv('UPLOAD_DIR', os.path.join(BASE_DIR, 'uploads'))
ALLOWED_EXTENSIONS = {'pdf'}

# PDF Processing Configuration
PDF_MAX_PAGES = 100  # Max pages to process
PDF_TEXT_MIN_LENGTH = 10  # Minimum characters required

# Model Inference Configuration
CONFIDENCE_THRESHOLD = 0.0  # Minimum confidence score
PREDICTION_TIMEOUT = 60  # Seconds

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', os.path.join(BASE_DIR, 'logs', 'ml_service.log'))

# Create necessary directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(os.path.dirname(STACK_MODEL_PATH), exist_ok=True)
