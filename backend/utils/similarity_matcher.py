import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityMatcher:
    def __init__(self, threshold=0.7):
        self.threshold = threshold
    
    def calculate_cosine_similarity(self, features1, features2):
        """Calculate cosine similarity between two feature vectors"""
        features1 = np.array(features1).reshape(1, -1)
        features2 = np.array(features2).reshape(1, -1)
        
        similarity = cosine_similarity(features1, features2)[0][0]
        return float(similarity)
    
    def find_matches(self, query_features, database_cases, top_k=5):
        """Find top matches from database"""
        matches = []
        
        for case in database_cases:
            if 'features' in case:
                similarity = self.calculate_cosine_similarity(
                    query_features, 
                    case['features']
                )
                
                if similarity >= self.threshold:
                    matches.append({
                        'case_id': case.get('id'),
                        'name': case.get('name'),
                        'age': case.get('age'),
                        'location': case.get('location'),
                        'similarity_score': similarity,
                        'image_path': case.get('image_path')
                    })
        
        # Sort by similarity score (descending)
        matches.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return matches[:top_k]
