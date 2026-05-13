import logging
import pickle
import numpy as np
from typing import Tuple, Dict, Any
from sentence_transformers import SentenceTransformer
import warnings

logger = logging.getLogger(__name__)
warnings.filterwarnings('ignore')


class MLModel:
    """Handles ML model loading and inference"""

    _instance = None
    _models_loaded = False

    def __new__(cls):
        """Singleton pattern to ensure only one instance"""
        if cls._instance is None:
            cls._instance = super(MLModel, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize ML model"""
        if not MLModel._models_loaded:
            self.embedding_model = None
            self.stack_model = None
            self.label_encoder = None
            self._load_models()

    def _load_models(self):
        """Load all required models"""
        try:
            logger.info("Loading embedding model...")
            self._load_embedding_model()
            logger.info("✓ Embedding model loaded successfully")

            logger.info("Loading stack model and label encoder...")
            self._load_pickle_models()
            logger.info("✓ Stack model and label encoder loaded successfully")

            MLModel._models_loaded = True
            logger.info("All models loaded successfully")

        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            raise Exception(f"Failed to load models: {str(e)}")

    def _load_embedding_model(self):
        """Load sentence transformer embedding model"""
        try:
            from config.settings import EMBEDDING_MODEL_NAME, DEVICE

            self.embedding_model = SentenceTransformer(
                EMBEDDING_MODEL_NAME,
                device=DEVICE
            )
            logger.info(f"Loaded embedding model: {EMBEDDING_MODEL_NAME} on device: {DEVICE}")

        except Exception as e:
            logger.error(f"Error loading embedding model: {str(e)}")
            raise Exception(f"Failed to load embedding model: {str(e)}")

    def _load_pickle_models(self):
        """Load stack model and label encoder from pickle files"""
        try:
            from config.settings import STACK_MODEL_PATH, LABEL_ENCODER_PATH
            import os

            # Load stack model
            if not os.path.exists(STACK_MODEL_PATH):
                raise FileNotFoundError(f"Stack model not found at {STACK_MODEL_PATH}")

            with open(STACK_MODEL_PATH, 'rb') as f:
                self.stack_model = pickle.load(f)
            logger.info(f"Loaded stack model from {STACK_MODEL_PATH}")

            # Load label encoder
            if not os.path.exists(LABEL_ENCODER_PATH):
                raise FileNotFoundError(f"Label encoder not found at {LABEL_ENCODER_PATH}")

            with open(LABEL_ENCODER_PATH, 'rb') as f:
                self.label_encoder = pickle.load(f)
            logger.info(f"Loaded label encoder from {LABEL_ENCODER_PATH}")

        except FileNotFoundError as fnf:
            logger.error(f"File not found: {str(fnf)}")
            raise Exception(f"Model files not found: {str(fnf)}")
        except Exception as e:
            logger.error(f"Error loading pickle models: {str(e)}")
            raise Exception(f"Failed to load pickle models: {str(e)}")

    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict document label from text

        Args:
            text: Extracted document text

        Returns:
            Tuple of (predicted_label, confidence_score)

        Raises:
            ValueError: If input is invalid
            Exception: If prediction fails
        """
        try:
            # Validate input
            if not text or len(text.strip()) < 10:
                raise ValueError("Input text is too short for prediction")

            # Generate embedding
            logger.info("Generating embeddings...")
            embedding = self._generate_embedding(text)
            logger.info(f"Embedding generated with shape: {embedding.shape}")

            # Make prediction
            logger.info("Making prediction...")
            prediction = self.stack_model.predict(embedding)
            confidence = self.stack_model.predict_proba(embedding)

            # Convert encoded label back to original label
            predicted_label_encoded = prediction[0]
            predicted_label = self._decode_label(predicted_label_encoded)

            # Get confidence score
            confidence_score = float(np.max(confidence[0]))

            logger.info(f"Prediction: {predicted_label}, Confidence: {confidence_score:.4f}")

            return predicted_label, confidence_score

        except ValueError as ve:
            logger.error(f"ValueError during prediction: {str(ve)}")
            raise ValueError(f"Prediction error: {str(ve)}")
        except Exception as e:
            logger.error(f"Error during prediction: {str(e)}")
            raise Exception(f"Prediction failed: {str(e)}")

    def _generate_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for text using sentence transformer

        Args:
            text: Input text

        Returns:
            Embedding as numpy array

        Raises:
            Exception: If embedding generation fails
        """
        try:
            if self.embedding_model is None:
                raise Exception("Embedding model not loaded")

            # Generate embedding
            embedding = self.embedding_model.encode(
                text,
                convert_to_numpy=True,
                show_progress_bar=False
            )

            # Reshape to 2D array (1, embedding_size) for model prediction
            embedding = embedding.reshape(1, -1)

            return embedding

        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            raise Exception(f"Failed to generate embedding: {str(e)}")

    def _decode_label(self, encoded_label: Any) -> str:
        """
        Decode label from encoded value back to original label

        Args:
            encoded_label: Encoded label value

        Returns:
            Original label string

        Raises:
            Exception: If decoding fails
        """
        try:
            if self.label_encoder is None:
                raise Exception("Label encoder not loaded")

            # Handle both single values and arrays
            if isinstance(encoded_label, np.ndarray):
                encoded_label = encoded_label[0] if len(encoded_label) > 0 else encoded_label

            # Decode label
            decoded_label = self.label_encoder.inverse_transform([encoded_label])
            label = str(decoded_label[0])

            return label

        except Exception as e:
            logger.error(f"Error decoding label: {str(e)}")
            raise Exception(f"Failed to decode label: {str(e)}")

    def is_ready(self) -> bool:
        """Check if all models are loaded and ready"""
        return (
            self.embedding_model is not None
            and self.stack_model is not None
            and self.label_encoder is not None
        )


# Global model instance
_model_instance = None


def get_model() -> MLModel:
    """Get global ML model instance (singleton)"""
    global _model_instance
    if _model_instance is None:
        _model_instance = MLModel()
    return _model_instance
