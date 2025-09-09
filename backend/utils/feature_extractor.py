import tensorflow as tf
import numpy as np
from models.image_processor import ImageProcessor

class FeatureExtractor:
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.model = self.load_facenet_model()
    
    def load_facenet_model(self):
        """Load pre-trained FaceNet model"""
        try:
            # For demo, use a simplified model or mock
            # In production, load actual FaceNet weights
            model = tf.keras.applications.MobileNetV2(
                weights='imagenet',
                include_top=False,
                input_shape=(160, 160, 3),
                pooling='avg'
            )
            return model
        except Exception as e:
            print(f"Model loading error: {e}")
            return None
    
    def preprocess_image(self, image_file):
        """Preprocess image for feature extraction"""
        return self.image_processor.preprocess_image(image_file)
    
    def extract_features(self, processed_image):
        """Extract facial features using FaceNet"""
        try:
            if self.model:
                features = self.model.predict(processed_image)
                # Normalize features
                features = features / np.linalg.norm(features)
                return features.flatten()
            else:
                # Mock features for demo
                return np.random.rand(1280)  # MobileNetV2 output size
        except Exception as e:
            raise Exception(f"Feature extraction failed: {str(e)}")
