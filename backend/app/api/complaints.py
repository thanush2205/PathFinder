"""
Complaints Management API Routes
Handle user complaints and queries
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List, Optional
from datetime import datetime
from ..models.schemas import (
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
    ComplaintStatus
)
from ..core.security import get_current_user, require_admin
from ..services.database import firebase_service

router = APIRouter(prefix="/complaints", tags=["Complaints"])


@router.post("/", response_model=ComplaintResponse, status_code=status.HTTP_201_CREATED)
async def create_complaint(
    complaint: ComplaintCreate,
    current_user: Dict = Depends(get_current_user)
):
    """
    Create a new complaint
    Users can only create complaints for themselves
    """
    user_id = current_user.get("sub")
    
    # Verify user is creating their own complaint (unless admin)
    if current_user.get("role") != "admin" and complaint.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create complaints for yourself"
        )
    
    # Create complaint data
    complaint_data = {
        "user_id": complaint.user_id,
        "message": complaint.message,
        "timestamp": datetime.utcnow().isoformat(),
        "status": ComplaintStatus.OPEN.value,
        "admin_response": None
    }
    
    try:
        complaint_id = firebase_service.create_complaint(complaint_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create complaint: {str(e)}"
        )
    
    return ComplaintResponse(
        id=complaint_id,
        user_id=complaint_data["user_id"],
        message=complaint_data["message"],
        timestamp=datetime.fromisoformat(complaint_data["timestamp"]),
        status=ComplaintStatus.OPEN
    )


@router.get("/my-complaints", response_model=List[ComplaintResponse])
async def get_my_complaints(current_user: Dict = Depends(get_current_user)):
    """
    Get all complaints for current user
    """
    user_id = current_user.get("sub")
    complaints = firebase_service.get_user_complaints(user_id)
    
    response_complaints = []
    for complaint in complaints:
        response_complaints.append(ComplaintResponse(
            id=complaint["id"],
            user_id=complaint["user_id"],
            message=complaint["message"],
            timestamp=datetime.fromisoformat(complaint["timestamp"]),
            status=ComplaintStatus(complaint.get("status", "open")),
            admin_response=complaint.get("admin_response")
        ))
    
    # Sort by timestamp (newest first)
    response_complaints.sort(key=lambda x: x.timestamp, reverse=True)
    
    return response_complaints


@router.get("/", response_model=List[ComplaintResponse])
async def get_all_complaints(
    status_filter: Optional[str] = None,
    current_user: Dict = Depends(require_admin)
):
    """
    Get all complaints (Admin only)
    Optionally filter by status
    """
    complaints = firebase_service.get_all_complaints(status=status_filter)
    
    response_complaints = []
    for complaint in complaints:
        response_complaints.append(ComplaintResponse(
            id=complaint["id"],
            user_id=complaint["user_id"],
            message=complaint["message"],
            timestamp=datetime.fromisoformat(complaint["timestamp"]),
            status=ComplaintStatus(complaint.get("status", "open")),
            admin_response=complaint.get("admin_response")
        ))
    
    # Sort by timestamp (newest first)
    response_complaints.sort(key=lambda x: x.timestamp, reverse=True)
    
    return response_complaints


@router.get("/{complaint_id}", response_model=ComplaintResponse)
async def get_complaint(
    complaint_id: str,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get a specific complaint
    """
    complaint = firebase_service.get_complaint(complaint_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    user_id = current_user.get("sub")
    complaint_user_id = complaint.get("user_id")
    
    # Verify access
    if current_user.get("role") != "admin" and complaint_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view your own complaints"
        )
    
    return ComplaintResponse(
        id=complaint_id,
        user_id=complaint["user_id"],
        message=complaint["message"],
        timestamp=datetime.fromisoformat(complaint["timestamp"]),
        status=ComplaintStatus(complaint.get("status", "open")),
        admin_response=complaint.get("admin_response")
    )


@router.patch("/{complaint_id}", response_model=ComplaintResponse)
async def update_complaint(
    complaint_id: str,
    updates: ComplaintUpdate,
    current_user: Dict = Depends(require_admin)
):
    """
    Update complaint status and add admin response (Admin only)
    """
    # Get existing complaint
    complaint = firebase_service.get_complaint(complaint_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # Prepare updates
    update_data = {
        "status": updates.status.value
    }
    
    if updates.admin_response:
        update_data["admin_response"] = updates.admin_response
    
    # Update complaint
    try:
        firebase_service.update_complaint(complaint_id, update_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update complaint: {str(e)}"
        )
    
    # Get updated complaint
    updated_complaint = firebase_service.get_complaint(complaint_id)
    
    return ComplaintResponse(
        id=complaint_id,
        user_id=updated_complaint["user_id"],
        message=updated_complaint["message"],
        timestamp=datetime.fromisoformat(updated_complaint["timestamp"]),
        status=ComplaintStatus(updated_complaint.get("status", "open")),
        admin_response=updated_complaint.get("admin_response")
    )


@router.delete("/{complaint_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_complaint(
    complaint_id: str,
    current_user: Dict = Depends(require_admin)
):
    """
    Delete a complaint (Admin only)
    """
    complaint = firebase_service.get_complaint(complaint_id)
    
    if not complaint:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Complaint not found"
        )
    
    # In production, implement actual deletion
    # For now, we can mark as closed
    try:
        firebase_service.update_complaint(complaint_id, {"status": "closed"})
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete complaint: {str(e)}"
        )
    
    return None
