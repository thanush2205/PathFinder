"""
Authentication API Routes
Handles user signup, login, token management
"""
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
import secrets
import string
from typing import Dict
from ..models.schemas import UserCreate, UserLogin, Token, UserResponse, UserRole
from ..core.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    get_current_user
)
from ..services.database import firebase_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


def generate_password(length: int = 12) -> str:
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password


@router.post("/signup", response_model=Token, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """
    Register a new user
    Supports both manual password and auto-generated password
    """
    # Check if user already exists
    existing_user = firebase_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Handle password
    if user.auto_generate_password:
        plain_password = generate_password()
    elif user.password:
        plain_password = user.password
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either provide a password or set auto_generate_password to True"
        )
    
    # Hash password
    hashed_password = hash_password(plain_password)
    
    # Create user data
    user_data = {
        "name": user.name,
        "email": user.email,
        "role": user.role.value,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow().isoformat()
    }
    
    # Save to database
    try:
        user_id = firebase_service.create_user(user_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )
    
    # Create tokens
    token_data = {
        "sub": user_id,
        "email": user.email,
        "role": user.role.value
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Create response
    user_response = UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        role=user.role,
        created_at=datetime.fromisoformat(user_data["created_at"])
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    """
    Login user with email and password
    Returns JWT access and refresh tokens
    """
    # Get user by email
    user_data = firebase_service.get_user_by_email(credentials.email)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user_data.get("hashed_password", "")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    user_id = user_data.get("id")
    user_role = user_data.get("role", "user")
    
    # Create tokens
    token_data = {
        "sub": user_id,
        "email": credentials.email,
        "role": user_role
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    # Create user response
    user_response = UserResponse(
        id=user_id,
        name=user_data.get("name", ""),
        email=user_data.get("email", ""),
        role=UserRole(user_role),
        created_at=datetime.fromisoformat(user_data.get("created_at", datetime.utcnow().isoformat()))
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict = Depends(get_current_user)):
    """Get current authenticated user information"""
    user_id = current_user.get("sub")
    user_data = firebase_service.get_user_by_id(user_id)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user_id,
        name=user_data.get("name", ""),
        email=user_data.get("email", ""),
        role=UserRole(user_data.get("role", "user")),
        created_at=datetime.fromisoformat(user_data.get("created_at", datetime.utcnow().isoformat()))
    )


@router.post("/refresh", response_model=Token)
async def refresh_access_token(current_user: Dict = Depends(get_current_user)):
    """
    Refresh access token using refresh token
    """
    user_id = current_user.get("sub")
    user_data = firebase_service.get_user_by_id(user_id)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Create new tokens
    token_data = {
        "sub": user_id,
        "email": user_data.get("email"),
        "role": user_data.get("role")
    }
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    user_response = UserResponse(
        id=user_id,
        name=user_data.get("name", ""),
        email=user_data.get("email", ""),
        role=UserRole(user_data.get("role", "user")),
        created_at=datetime.fromisoformat(user_data.get("created_at", datetime.utcnow().isoformat()))
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_response
    )
