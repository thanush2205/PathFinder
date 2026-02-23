"""
Pydantic models for data validation and serialization
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    """User roles"""
    USER = "user"
    ADMIN = "admin"


class ComplaintStatus(str, Enum):
    """Complaint status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


# ============= User Models =============

class UserBase(BaseModel):
    """Base user model"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: UserRole = UserRole.USER


class UserCreate(UserBase):
    """User creation model"""
    password: Optional[str] = None
    auto_generate_password: bool = False


class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """User response model"""
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserInDB(UserBase):
    """User in database"""
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None


# ============= Token Models =============

class Token(BaseModel):
    """Token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    """Token payload data"""
    sub: str
    email: str
    role: str


# ============= Session Models =============

class SessionBase(BaseModel):
    """Base session model"""
    user_id: str


class SessionCreate(SessionBase):
    """Session creation model"""
    pass


class SessionUpdate(BaseModel):
    """Session update model"""
    hazards_detected: Optional[List[str]] = None
    end_time: Optional[datetime] = None


class SessionResponse(SessionBase):
    """Session response model"""
    id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    hazards_detected: List[str] = []
    duration_seconds: Optional[int] = None
    
    class Config:
        from_attributes = True


# ============= Complaint Models =============

class ComplaintBase(BaseModel):
    """Base complaint model"""
    message: str = Field(..., min_length=10, max_length=1000)


class ComplaintCreate(ComplaintBase):
    """Complaint creation model"""
    user_id: str


class ComplaintUpdate(BaseModel):
    """Complaint update model"""
    status: ComplaintStatus
    admin_response: Optional[str] = None


class ComplaintResponse(ComplaintBase):
    """Complaint response model"""
    id: str
    user_id: str
    timestamp: datetime
    status: ComplaintStatus = ComplaintStatus.OPEN
    admin_response: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============= Detection Models =============

class DetectionResult(BaseModel):
    """Object detection result"""
    class_name: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]
    distance: Optional[float] = None
    direction: Optional[str] = None  # left, right, center


class NavigationAlert(BaseModel):
    """Navigation alert for user"""
    alert_type: str  # obstacle, vehicle, person, etc.
    message: str
    severity: str  # low, medium, high
    detections: List[DetectionResult]


# ============= Analytics Models =============

class UserAnalytics(BaseModel):
    """User analytics data"""
    total_users: int
    active_users_today: int
    active_users_week: int
    new_users_today: int


class SessionAnalytics(BaseModel):
    """Session analytics data"""
    total_sessions: int
    sessions_today: int
    average_duration_minutes: float
    total_hazards_detected: int


class HazardAnalytics(BaseModel):
    """Hazard detection analytics"""
    hazard_type: str
    count: int


class ComplaintAnalytics(BaseModel):
    """Complaint analytics"""
    total_complaints: int
    open_complaints: int
    resolved_complaints: int
    average_resolution_time_hours: float


class DashboardAnalytics(BaseModel):
    """Complete dashboard analytics"""
    users: UserAnalytics
    sessions: SessionAnalytics
    hazards: List[HazardAnalytics]
    complaints: ComplaintAnalytics
    system_efficiency: Dict[str, Any]


# ============= Voice Assistant Models =============

class VoiceCommand(BaseModel):
    """Voice command input"""
    audio_data: Optional[str] = None  # base64 encoded audio
    text: Optional[str] = None  # text input
    

class VoiceResponse(BaseModel):
    """Voice assistant response"""
    text: str
    audio_url: Optional[str] = None
    action: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
