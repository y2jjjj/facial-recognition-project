from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from database.db_operations import DatabaseManager
from utils.feature_extractor import FeatureExtractor
from utils.similarity_matcher import SimilarityMatcher

app = Flask(__name__)
CORS(app)

# Initialize components
db_manager = DatabaseManager()
feature_extractor = FeatureExtractor()
similarity_matcher = SimilarityMatcher()

@app.route('/api/upload-case', methods=['POST'])
def upload_case():
    try:
        # Get form data
        name = request.form.get('name')
        age = request.form.get('age')
        location = request.form.get('location')
        image = request.files.get('image')
        
        # Process image and extract features
        processed_image = feature_extractor.preprocess_image(image)
        features = feature_extractor.extract_features(processed_image)
        
        # Save to database
        case_id = db_manager.save_case({
            'name': name,
            'age': age,
            'location': location,
            'features': features.tolist(),
            'image_path': f'uploads/{image.filename}'
        })
        
        return jsonify({'success': True, 'case_id': case_id})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/match-image', methods=['POST'])
def match_image():
    try:
        image = request.files.get('image')
        
        # Extract features from uploaded image
        processed_image = feature_extractor.preprocess_image(image)
        query_features = feature_extractor.extract_features(processed_image)
        
        # Get all cases from database
        all_cases = db_manager.get_all_cases()
        
        # Find matches
        matches = similarity_matcher.find_matches(query_features, all_cases)
        
        return jsonify({'success': True, 'matches': matches})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
