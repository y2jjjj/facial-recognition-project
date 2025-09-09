import firebase_admin
from firebase_admin import credentials, firestore
import uuid
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.db = self.initialize_firebase()
    
    def initialize_firebase(self):
        """Initialize Firebase connection"""
        try:
            # For demo, use mock database or local storage
            # In production, use actual Firebase credentials
            if not firebase_admin._apps:
                # Mock initialization for demo
                print("Using mock database for demo")
                return MockDatabase()
            return firestore.client()
        except Exception as e:
            print(f"Database initialization error: {e}")
            return MockDatabase()
    
    def save_case(self, case_data):
        """Save missing person case to database"""
        try:
            case_id = str(uuid.uuid4())
            case_data.update({
                'id': case_id,
                'created_at': datetime.now().isoformat(),
                'status': 'active'
            })
            
            # Save to database
            self.db.collection('missing_persons').document(case_id).set(case_data)
            return case_id
        except Exception as e:
            raise Exception(f"Database save error: {str(e)}")
    
    def get_all_cases(self):
        """Retrieve all missing person cases"""
        try:
            cases = []
            docs = self.db.collection('missing_persons').stream()
            
            for doc in docs:
                case_data = doc.to_dict()
                cases.append(case_data)
            
            return cases
        except Exception as e:
            raise Exception(f"Database retrieval error: {str(e)}")
    
    def get_case_by_id(self, case_id):
        """Get specific case by ID"""
        try:
            doc = self.db.collection('missing_persons').document(case_id).get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            raise Exception(f"Database query error: {str(e)}")

class MockDatabase:
    """Mock database for demo purposes"""
    def __init__(self):
        self.data = {'missing_persons': {}}
    
    def collection(self, collection_name):
        return MockCollection(self.data.get(collection_name, {}))

class MockCollection:
    def __init__(self, data):
        self.data = data
    
    def document(self, doc_id):
        return MockDocument(self.data, doc_id)
    
    def stream(self):
        for doc_id, doc_data in self.data.items():
            yield MockDoc(doc_id, doc_data)

class MockDocument:
    def __init__(self, collection_data, doc_id):
        self.collection_data = collection_data
        self.doc_id = doc_id
    
    def set(self, data):
        self.collection_data[self.doc_id] = data
    
    def get(self):
        return MockDoc(self.doc_id, self.collection_data.get(self.doc_id))

class MockDoc:
    def __init__(self, doc_id, data):
        self.id = doc_id
        self.data = data
    
    @property
    def exists(self):
        return self.data is not None
    
    def to_dict(self):
        return self.data if self.data else {}
