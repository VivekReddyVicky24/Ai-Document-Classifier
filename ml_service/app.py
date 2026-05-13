import os
import sys
import logging
from datetime import datetime
from functools import wraps

# Add config to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import traceback

# Import configuration
from config.settings import (
    DEBUG, ENV, SECRET_KEY, HOST, PORT, THREADED,
    MAX_FILE_SIZE, UPLOAD_DIR, ALLOWED_EXTENSIONS,
    LOG_LEVEL, LOG_FILE, PDF_MAX_PAGES, PDF_TEXT_MIN_LENGTH
)

# Import utilities
from utils.pdf_processor import PDFProcessor
from utils.ml_model import get_model

# ==========================================
# Logging Configuration
# ==========================================

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==========================================
# Flask App Initialization
# ==========================================

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['JSON_SORT_KEYS'] = False

# Enable CORS
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# ==========================================
# Global Model Instance
# ==========================================

ml_model = None
model_initialized = False
model_init_error = None


def initialize_model():
    """Initialize ML model on app startup"""
    global ml_model, model_initialized, model_init_error
    try:
        logger.info("Initializing ML model...")
        ml_model = get_model()
        if ml_model.is_ready():
            model_initialized = True
            logger.info("✓ ML model initialized successfully")
        else:
            raise Exception("Model failed to load - not all components ready")
    except Exception as e:
        logger.error(f"✗ Failed to initialize ML model: {str(e)}")
        model_init_error = str(e)
        model_initialized = False


def require_model(f):
    """Decorator to check if model is initialized"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not model_initialized:
            return jsonify({
                "success": False,
                "message": "ML model not ready. Please try again later.",
                "error": model_init_error
            }), 503
        return f(*args, **kwargs)
    return decorated_function


# ==========================================
# Health Check Endpoints
# ==========================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy",
        "service": "AI Document Classifier ML Service",
        "timestamp": datetime.utcnow().isoformat(),
        "model_status": "ready" if model_initialized else "initializing"
    }), 200


@app.route('/health/detailed', methods=['GET'])
def health_check_detailed():
    """Detailed health check endpoint"""
    return jsonify({
        "success": True,
        "status": "healthy" if model_initialized else "degraded",
        "service": "AI Document Classifier ML Service",
        "environment": ENV,
        "debug_mode": DEBUG,
        "model_initialized": model_initialized,
        "model_error": model_init_error,
        "timestamp": datetime.utcnow().isoformat(),
        "embedding_model": "BAAI/bge-large-en-v1.5",
        "api_version": "1.0.0"
    }), 200


# ==========================================
# Prediction Endpoints
# ==========================================

def allowed_file(filename):
    """Check if file is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def validate_file_upload():
    """Validate file upload request"""
    # Check if file is in request
    if 'file' not in request.files:
        return None, "No file provided"

    file = request.files['file']

    # Check if file has filename
    if file.filename == '':
        return None, "No file selected"

    # Check if file is PDF
    if not allowed_file(file.filename):
        return None, "Only PDF files are allowed"

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return None, f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"

    if file_size == 0:
        return None, "File is empty"

    return file, None


@app.route('/api/predict', methods=['POST', 'OPTIONS'])
@require_model
def predict():
    """
    Predict document label from PDF file

    Request: POST /api/predict
    Content-Type: multipart/form-data
    Body: file (PDF file)

    Response: JSON with predicted_label and confidence
    """
    try:
        logger.info("Received prediction request")

        # Validate file upload
        file, error = validate_file_upload()
        if error:
            logger.warning(f"File validation error: {error}")
            return jsonify({
                "success": False,
                "message": error
            }), 400

        # Read file bytes
        try:
            file_bytes = file.read()
            filename = secure_filename(file.filename)
            logger.info(f"Processing file: {filename} ({len(file_bytes)} bytes)")
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            return jsonify({
                "success": False,
                "message": "Error reading file"
            }), 400

        # Extract text from PDF
        try:
            logger.info("Extracting text from PDF...")
            extracted_text, num_pages = PDFProcessor.extract_text_from_pdf(
                file_bytes,
                max_pages=PDF_MAX_PAGES
            )
            logger.info(f"Extracted {len(extracted_text)} characters from {num_pages} pages")
        except ValueError as ve:
            logger.warning(f"PDF validation error: {str(ve)}")
            return jsonify({
                "success": False,
                "message": f"PDF processing error: {str(ve)}"
            }), 400
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return jsonify({
                "success": False,
                "message": "Error extracting text from PDF"
            }), 500

        # Make prediction
        try:
            logger.info("Making prediction...")
            predicted_label, confidence = ml_model.predict(extracted_text)
            logger.info(f"Prediction completed: {predicted_label} ({confidence:.4f})")
        except ValueError as ve:
            logger.warning(f"Prediction validation error: {str(ve)}")
            return jsonify({
                "success": False,
                "message": f"Prediction error: {str(ve)}"
            }), 400
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({
                "success": False,
                "message": "Error making prediction"
            }), 500

        # Return successful response
        response = {
            "success": True,
            "message": "Prediction successful",
            "data": {
                "predicted_label": predicted_label,
                "confidence": round(confidence, 4),
                "filename": filename,
                "pages_processed": num_pages,
                "text_length": len(extracted_text),
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        logger.info(f"Returning prediction response: {predicted_label}")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            "success": False,
            "message": "Unexpected server error"
        }), 500


@app.route('/api/predict/batch', methods=['POST', 'OPTIONS'])
@require_model
def predict_batch():
    """
    Batch prediction endpoint (for future use)

    Request: POST /api/predict/batch
    Content-Type: multipart/form-data
    Body: files[] (multiple PDF files)

    Response: JSON with list of predictions
    """
    try:
        logger.info("Received batch prediction request")

        # Check if files are in request
        if 'files' not in request.files:
            return jsonify({
                "success": False,
                "message": "No files provided"
            }), 400

        files = request.files.getlist('files')

        if not files or len(files) == 0:
            return jsonify({
                "success": False,
                "message": "No files selected"
            }), 400

        # Limit batch size
        max_batch_size = 10
        if len(files) > max_batch_size:
            return jsonify({
                "success": False,
                "message": f"Too many files. Maximum: {max_batch_size}"
            }), 400

        predictions = []
        errors = []

        # Process each file
        for idx, file in enumerate(files):
            try:
                if not allowed_file(file.filename):
                    errors.append({
                        "file": file.filename,
                        "error": "Invalid file type"
                    })
                    continue

                # Read file bytes
                file_bytes = file.read()
                filename = secure_filename(file.filename)

                # Extract text
                extracted_text, num_pages = PDFProcessor.extract_text_from_pdf(
                    file_bytes,
                    max_pages=PDF_MAX_PAGES
                )

                # Make prediction
                predicted_label, confidence = ml_model.predict(extracted_text)

                predictions.append({
                    "filename": filename,
                    "predicted_label": predicted_label,
                    "confidence": round(confidence, 4),
                    "pages_processed": num_pages
                })

                logger.info(f"Batch prediction {idx + 1}/{len(files)}: {predicted_label}")

            except Exception as e:
                logger.error(f"Error processing file {idx + 1}: {str(e)}")
                errors.append({
                    "file": file.filename,
                    "error": str(e)
                })

        response = {
            "success": len(errors) == 0,
            "message": f"Processed {len(predictions)} files",
            "data": {
                "predictions": predictions,
                "errors": errors if errors else None,
                "total_files": len(files),
                "successful": len(predictions),
                "failed": len(errors),
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Unexpected error in batch predict: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Unexpected server error"
        }), 500


# ==========================================
# Information Endpoints
# ==========================================

@app.route('/api/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        "success": True,
        "service": "AI Document Classifier ML Service",
        "version": "1.0.0",
        "description": "Flask-based ML inference API for document classification",
        "endpoints": {
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "Health check"
            },
            "health_detailed": {
                "method": "GET",
                "path": "/health/detailed",
                "description": "Detailed health check"
            },
            "predict": {
                "method": "POST",
                "path": "/api/predict",
                "description": "Predict document label from PDF",
                "content_type": "multipart/form-data",
                "parameters": {
                    "file": "PDF file (required)"
                }
            },
            "batch_predict": {
                "method": "POST",
                "path": "/api/predict/batch",
                "description": "Batch predict multiple PDFs",
                "content_type": "multipart/form-data",
                "parameters": {
                    "files": "Multiple PDF files (required)"
                }
            },
            "info": {
                "method": "GET",
                "path": "/api/info",
                "description": "API information"
            }
        },
        "models": {
            "embedding_model": "BAAI/bge-large-en-v1.5",
            "stack_model": "stack_model.pkl",
            "label_encoder": "label_encoder.pkl"
        },
        "features": {
            "pdf_text_extraction": True,
            "batch_processing": True,
            "cors_enabled": True,
            "model_singleton": True
        },
        "configuration": {
            "max_file_size_mb": MAX_FILE_SIZE / (1024 * 1024),
            "max_pdf_pages": PDF_MAX_PAGES,
            "min_text_length": PDF_TEXT_MIN_LENGTH,
            "environment": ENV,
            "debug": DEBUG
        }
    }), 200


# ==========================================
# Error Handlers
# ==========================================

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    logger.warning("Request entity too large")
    return jsonify({
        "success": False,
        "message": f"File too large. Maximum size: {MAX_FILE_SIZE / (1024*1024):.1f}MB"
    }), 413


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "success": False,
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors"""
    return jsonify({
        "success": False,
        "message": "Method not allowed"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        "success": False,
        "message": "Internal server error"
    }), 500


# ==========================================
# Application Startup
# ==========================================

@app.before_request
def before_request():
    """Before request processing"""
    logger.debug(f"{request.method} {request.path}")


@app.after_request
def after_request(response):
    """After request processing"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


# ==========================================
# Main Entry Point
# ==========================================

if __name__ == '__main__':
    try:
        logger.info("=" * 60)
        logger.info("Starting AI Document Classifier ML Service")
        logger.info("=" * 60)

        # Initialize model
        initialize_model()

        # Start Flask app
        if model_initialized:
            logger.info(f"Starting Flask server on {HOST}:{PORT}")
            logger.info(f"Environment: {ENV}")
            logger.info(f"Debug: {DEBUG}")
            logger.info("=" * 60)

            app.run(
                host=HOST,
                port=PORT,
                debug=DEBUG,
                threaded=THREADED
            )
        else:
            logger.error("Cannot start server - ML model failed to initialize")
            logger.error(f"Error: {model_init_error}")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Shutdown signal received")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        logger.error(traceback.format_exc())
        sys.exit(1)
