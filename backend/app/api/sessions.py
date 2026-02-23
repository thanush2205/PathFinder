"""
Session Management API Routes
Handle user navigation sessions
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List
from datetime import datetime
from ..models.schemas import SessionCreate, SessionUpdate, SessionResponse
from ..core.security import get_current_user, require_admin
from ..services.database import firebase_service

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(
    session: SessionCreate,
    current_user: Dict = Depends(get_current_user)
):
    """
    Start a new navigation session
    Users can only start sessions for themselves
    """
    user_id = current_user.get("sub")
    
    # Verify user is starting their own session (unless admin)
    if current_user.get("role") != "admin" and session.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only start sessions for yourself"
        )
    
    # Create session data
    session_data = {
        "user_id": session.user_id,
        "start_time": datetime.utcnow().isoformat(),
        "end_time": None,
        "hazards_detected": [],
        "duration_seconds": None
    }
    
    try:
        session_id = firebase_service.create_session(session_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )
    
    return SessionResponse(
        id=session_id,
        user_id=session_data["user_id"],
        start_time=datetime.fromisoformat(session_data["start_time"]),
        hazards_detected=[]
    )


@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: str,
    updates: SessionUpdate,
    current_user: Dict = Depends(get_current_user)
):
    """
    Update a session (add hazards or end session)
    """
    # Get existing session
    session_data = firebase_service.get_session(session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    user_id = current_user.get("sub")
    session_user_id = session_data.get("user_id")
    
    # Verify user owns this session (unless admin)
    if current_user.get("role") != "admin" and session_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own sessions"
        )
    
    # Prepare updates
    update_data = {}
    
    if updates.hazards_detected is not None:
        # Append new hazards
        existing_hazards = session_data.get("hazards_detected", [])
        update_data["hazards_detected"] = existing_hazards + updates.hazards_detected
    
    if updates.end_time is not None:
        update_data["end_time"] = updates.end_time.isoformat()
        
        # Calculate duration
        start_time = datetime.fromisoformat(session_data["start_time"])
        duration = (updates.end_time - start_time).total_seconds()
        update_data["duration_seconds"] = int(duration)
    
    # Update session
    try:
        firebase_service.update_session(session_id, update_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update session: {str(e)}"
        )
    
    # Get updated session
    updated_session = firebase_service.get_session(session_id)
    
    return SessionResponse(
        id=session_id,
        user_id=updated_session["user_id"],
        start_time=datetime.fromisoformat(updated_session["start_time"]),
        end_time=datetime.fromisoformat(updated_session["end_time"]) if updated_session.get("end_time") else None,
        hazards_detected=updated_session.get("hazards_detected", []),
        duration_seconds=updated_session.get("duration_seconds")
    )


@router.get("/my-sessions", response_model=List[SessionResponse])
async def get_my_sessions(
    limit: int = 50,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get all sessions for current user
    """
    user_id = current_user.get("sub")
    sessions = firebase_service.get_user_sessions(user_id, limit=limit)
    
    response_sessions = []
    for session in sessions:
        response_sessions.append(SessionResponse(
            id=session["id"],
            user_id=session["user_id"],
            start_time=datetime.fromisoformat(session["start_time"]),
            end_time=datetime.fromisoformat(session["end_time"]) if session.get("end_time") else None,
            hazards_detected=session.get("hazards_detected", []),
            duration_seconds=session.get("duration_seconds")
        ))
    
    return response_sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get a specific session
    """
    session = firebase_service.get_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    user_id = current_user.get("sub")
    session_user_id = session.get("user_id")
    
    # Verify access
    if current_user.get("role") != "admin" and session_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own sessions"
        )
    
    return SessionResponse(
        id=session_id,
        user_id=session["user_id"],
        start_time=datetime.fromisoformat(session["start_time"]),
        end_time=datetime.fromisoformat(session["end_time"]) if session.get("end_time") else None,
        hazards_detected=session.get("hazards_detected", []),
        duration_seconds=session.get("duration_seconds")
    )


@router.get("/", response_model=List[SessionResponse])
async def get_all_sessions(
    limit: int = 100,
    current_user: Dict = Depends(require_admin)
):
    """
    Get all sessions (Admin only)
    """
    sessions = firebase_service.get_all_sessions(limit=limit)
    
    response_sessions = []
    for session in sessions:
        response_sessions.append(SessionResponse(
            id=session["id"],
            user_id=session["user_id"],
            start_time=datetime.fromisoformat(session["start_time"]),
            end_time=datetime.fromisoformat(session["end_time"]) if session.get("end_time") else None,
            hazards_detected=session.get("hazards_detected", []),
            duration_seconds=session.get("duration_seconds")
        ))
    
    return response_sessions
