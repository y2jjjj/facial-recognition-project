import cv2
import numpy as np
from PIL import Image

class ImageProcessor:
    def __init__(self):
        self.target_size = (160, 160)  # FaceNet input size
    
    def preprocess_image(self, image_file):
        """Preprocess uploaded image for FaceNet"""
        try:
            # Read image
            image = Image.open(image_file)
            image = image.convert('RGB')
            
            # Resize to target size
            image = image.resize(self.target_size)
            
            # Convert to numpy array and normalize
            image_array = np.array(image)
            image_array = image_array.astype('float32')
            image_array = (image_array - 127.5) / 128.0
            
            return np.expand_dims(image_array, axis=0)
        except Exception as e:
            raise Exception(f"Image preprocessing failed: {str(e)}")
    
    def detect_face(self, image_path):
        """Basic face detection using OpenCV"""
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) > 0:
            return faces[0]  # Return first detected face
        return None
