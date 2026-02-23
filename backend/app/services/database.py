"""
Firebase Database Service
Handles all database operations for PathFinder
"""
import firebase_admin
from firebase_admin import credentials, db, storage
from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)


class FirebaseService:
    """Firebase service for database operations"""
    
    def __init__(self):
        """Initialize Firebase"""
        self._initialized = False
        
    def initialize(self):
        """Initialize Firebase app"""
        if self._initialized:
            return
            
        try:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': settings.FIREBASE_DATABASE_URL,
                'storageBucket': settings.FIREBASE_STORAGE_BUCKET
            })
            self._initialized = True
            logger.info("Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            # For development, we can work without Firebase
            logger.warning("Running without Firebase connection")
    
    # ============= User Operations =============
    
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user"""
        try:
            ref = db.reference('users')
            user_ref = ref.push(user_data)
            return user_ref.key
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            ref = db.reference(f'users/{user_id}')
            return ref.get()
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            ref = db.reference('users')
            users = ref.order_by_child('email').equal_to(email).get()
            if users:
                user_id = list(users.keys())[0]
                user_data = users[user_id]
                user_data['id'] = user_id
                return user_data
            return None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user data"""
        try:
            ref = db.reference(f'users/{user_id}')
            ref.update(updates)
            return True
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            return False
    
    def get_all_users(self, role: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all users, optionally filtered by role"""
        try:
            ref = db.reference('users')
            users = ref.get()
            
            if not users:
                return []
            
            result = []
            for user_id, user_data in users.items():
                if role and user_data.get('role') != role:
                    continue
                user_data['id'] = user_id
                result.append(user_data)
            
            return result
        except Exception as e:
            logger.error(f"Error getting users: {e}")
            return []
    
    # ============= Session Operations =============
    
    def create_session(self, session_data: Dict[str, Any]) -> str:
        """Create a new session"""
        try:
            ref = db.reference('sessions')
            session_ref = ref.push(session_data)
            return session_ref.key
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            raise
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        try:
            ref = db.reference(f'sessions/{session_id}')
            return ref.get()
        except Exception as e:
            logger.error(f"Error getting session: {e}")
            return None
    
    def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session data"""
        try:
            ref = db.reference(f'sessions/{session_id}')
            ref.update(updates)
            return True
        except Exception as e:
            logger.error(f"Error updating session: {e}")
            return False
    
    def get_user_sessions(self, user_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all sessions for a user"""
        try:
            ref = db.reference('sessions')
            sessions = ref.order_by_child('user_id').equal_to(user_id).limit_to_last(limit).get()
            
            if not sessions:
                return []
            
            result = []
            for session_id, session_data in sessions.items():
                session_data['id'] = session_id
                result.append(session_data)
            
            return result
        except Exception as e:
            logger.error(f"Error getting user sessions: {e}")
            return []
    
    def get_all_sessions(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all sessions"""
        try:
            ref = db.reference('sessions')
            sessions = ref.limit_to_last(limit).get()
            
            if not sessions:
                return []
            
            result = []
            for session_id, session_data in sessions.items():
                session_data['id'] = session_id
                result.append(session_data)
            
            return result
        except Exception as e:
            logger.error(f"Error getting sessions: {e}")
            return []
    
    # ============= Complaint Operations =============
    
    def create_complaint(self, complaint_data: Dict[str, Any]) -> str:
        """Create a new complaint"""
        try:
            ref = db.reference('complaints')
            complaint_ref = ref.push(complaint_data)
            return complaint_ref.key
        except Exception as e:
            logger.error(f"Error creating complaint: {e}")
            raise
    
    def get_complaint(self, complaint_id: str) -> Optional[Dict[str, Any]]:
        """Get complaint by ID"""
        try:
            ref = db.reference(f'complaints/{complaint_id}')
            return ref.get()
        except Exception as e:
            logger.error(f"Error getting complaint: {e}")
            return None
    
    def update_complaint(self, complaint_id: str, updates: Dict[str, Any]) -> bool:
        """Update complaint"""
        try:
            ref = db.reference(f'complaints/{complaint_id}')
            ref.update(updates)
            return True
        except Exception as e:
            logger.error(f"Error updating complaint: {e}")
            return False
    
    def get_user_complaints(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all complaints for a user"""
        try:
            ref = db.reference('complaints')
            complaints = ref.order_by_child('user_id').equal_to(user_id).get()
            
            if not complaints:
                return []
            
            result = []
            for complaint_id, complaint_data in complaints.items():
                complaint_data['id'] = complaint_id
                result.append(complaint_data)
            
            return result
        except Exception as e:
            logger.error(f"Error getting user complaints: {e}")
            return []
    
    def get_all_complaints(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all complaints, optionally filtered by status"""
        try:
            ref = db.reference('complaints')
            
            if status:
                complaints = ref.order_by_child('status').equal_to(status).get()
            else:
                complaints = ref.get()
            
            if not complaints:
                return []
            
            result = []
            for complaint_id, complaint_data in complaints.items():
                complaint_data['id'] = complaint_id
                result.append(complaint_data)
            
            return result
        except Exception as e:
            logger.error(f"Error getting complaints: {e}")
            return []


# Global Firebase service instance
firebase_service = FirebaseService()
