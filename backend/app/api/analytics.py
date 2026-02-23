"""
Analytics API Routes
Admin dashboard analytics and system metrics
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, List
from datetime import datetime, timedelta
from collections import Counter
from ..models.schemas import (
    DashboardAnalytics,
    UserAnalytics,
    SessionAnalytics,
    HazardAnalytics,
    ComplaintAnalytics
)
from ..core.security import require_admin, get_current_user
from ..services.database import firebase_service

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardAnalytics)
async def get_dashboard_analytics(current_user: Dict = Depends(require_admin)):
    """
    Get complete dashboard analytics for admin
    Requires admin role
    """
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    
    # Get all data
    all_users = firebase_service.get_all_users()
    all_sessions = firebase_service.get_all_sessions()
    all_complaints = firebase_service.get_all_complaints()
    
    # === User Analytics ===
    total_users = len(all_users)
    
    # Count users by activity
    active_today = 0
    active_week = 0
    new_today = 0
    
    for user in all_users:
        created_at_str = user.get("created_at")
        if created_at_str:
            created_at = datetime.fromisoformat(created_at_str)
            if created_at >= today_start:
                new_today += 1
    
    # Count active users from sessions
    today_user_ids = set()
    week_user_ids = set()
    
    for session in all_sessions:
        start_time_str = session.get("start_time")
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
            user_id = session.get("user_id")
            
            if start_time >= today_start:
                today_user_ids.add(user_id)
            if start_time >= week_start:
                week_user_ids.add(user_id)
    
    active_today = len(today_user_ids)
    active_week = len(week_user_ids)
    
    user_analytics = UserAnalytics(
        total_users=total_users,
        active_users_today=active_today,
        active_users_week=active_week,
        new_users_today=new_today
    )
    
    # === Session Analytics ===
    total_sessions = len(all_sessions)
    sessions_today = 0
    total_duration = 0
    total_hazards = 0
    hazard_counter = Counter()
    
    for session in all_sessions:
        start_time_str = session.get("start_time")
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
            
            if start_time >= today_start:
                sessions_today += 1
            
            # Calculate duration
            end_time_str = session.get("end_time")
            if end_time_str:
                end_time = datetime.fromisoformat(end_time_str)
                duration = (end_time - start_time).total_seconds()
                total_duration += duration
            
            # Count hazards
            hazards = session.get("hazards_detected", [])
            total_hazards += len(hazards)
            hazard_counter.update(hazards)
    
    avg_duration = (total_duration / total_sessions / 60) if total_sessions > 0 else 0
    
    session_analytics = SessionAnalytics(
        total_sessions=total_sessions,
        sessions_today=sessions_today,
        average_duration_minutes=round(avg_duration, 2),
        total_hazards_detected=total_hazards
    )
    
    # === Hazard Analytics ===
    hazard_analytics = [
        HazardAnalytics(hazard_type=hazard, count=count)
        for hazard, count in hazard_counter.most_common(10)
    ]
    
    # === Complaint Analytics ===
    total_complaints = len(all_complaints)
    open_complaints = sum(1 for c in all_complaints if c.get("status") == "open")
    resolved_complaints = sum(1 for c in all_complaints if c.get("status") == "resolved")
    
    # Calculate average resolution time
    resolution_times = []
    for complaint in all_complaints:
        if complaint.get("status") == "resolved":
            timestamp_str = complaint.get("timestamp")
            # In production, track resolution_time in database
            # For now, use placeholder
            resolution_times.append(24)  # placeholder hours
    
    avg_resolution = (sum(resolution_times) / len(resolution_times)) if resolution_times else 0
    
    complaint_analytics = ComplaintAnalytics(
        total_complaints=total_complaints,
        open_complaints=open_complaints,
        resolved_complaints=resolved_complaints,
        average_resolution_time_hours=round(avg_resolution, 2)
    )
    
    # === System Efficiency ===
    system_efficiency = {
        "average_response_time_ms": 150,  # Mock data
        "detection_fps": 18,  # Mock data
        "api_uptime_percent": 99.9,  # Mock data
        "average_alert_delay_ms": 200  # Mock data
    }
    
    return DashboardAnalytics(
        users=user_analytics,
        sessions=session_analytics,
        hazards=hazard_analytics,
        complaints=complaint_analytics,
        system_efficiency=system_efficiency
    )


@router.get("/users/trend")
async def get_user_trend(days: int = 7, current_user: Dict = Depends(require_admin)):
    """
    Get user registration trend over specified days
    """
    all_users = firebase_service.get_all_users()
    now = datetime.utcnow()
    
    # Create daily buckets
    trend_data = []
    for i in range(days):
        date = now - timedelta(days=days - i - 1)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)
        
        count = 0
        for user in all_users:
            created_at_str = user.get("created_at")
            if created_at_str:
                created_at = datetime.fromisoformat(created_at_str)
                if date_start <= created_at < date_end:
                    count += 1
        
        trend_data.append({
            "date": date_start.strftime("%Y-%m-%d"),
            "count": count
        })
    
    return {"trend": trend_data}


@router.get("/sessions/trend")
async def get_session_trend(days: int = 7, current_user: Dict = Depends(require_admin)):
    """
    Get session activity trend over specified days
    """
    all_sessions = firebase_service.get_all_sessions()
    now = datetime.utcnow()
    
    # Create daily buckets
    trend_data = []
    for i in range(days):
        date = now - timedelta(days=days - i - 1)
        date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        date_end = date_start + timedelta(days=1)
        
        count = 0
        for session in all_sessions:
            start_time_str = session.get("start_time")
            if start_time_str:
                start_time = datetime.fromisoformat(start_time_str)
                if date_start <= start_time < date_end:
                    count += 1
        
        trend_data.append({
            "date": date_start.strftime("%Y-%m-%d"),
            "count": count
        })
    
    return {"trend": trend_data}


@router.get("/hazards/distribution")
async def get_hazard_distribution(current_user: Dict = Depends(require_admin)):
    """
    Get distribution of different hazard types
    """
    all_sessions = firebase_service.get_all_sessions()
    hazard_counter = Counter()
    
    for session in all_sessions:
        hazards = session.get("hazards_detected", [])
        hazard_counter.update(hazards)
    
    distribution = [
        {"hazard_type": hazard, "count": count, "percentage": 0}
        for hazard, count in hazard_counter.most_common()
    ]
    
    total = sum(item["count"] for item in distribution)
    if total > 0:
        for item in distribution:
            item["percentage"] = round((item["count"] / total) * 100, 2)
    
    return {"distribution": distribution}
