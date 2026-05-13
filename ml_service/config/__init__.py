"""
ML Service Configuration Module
"""

from .settings import *

__all__ = [
    'DEBUG',
    'ENV',
    'SECRET_KEY',
    'HOST',
    'PORT',
    'THREADING',
    'EMBEDDING_MODEL_NAME',
    'STACK_MODEL_PATH',
    'LABEL_ENCODER_PATH',
    'DEVICE',
    'MAX_FILE_SIZE',
    'UPLOAD_DIR',
    'ALLOWED_EXTENSIONS',
    'PDF_MAX_PAGES',
    'PDF_TEXT_MIN_LENGTH',
    'LOG_LEVEL',
    'LOG_FILE',
]
