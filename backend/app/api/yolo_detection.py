from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from ..services.yolo_detection import yolo_detector
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class DetectionRequest(BaseModel):
    image: str  # Base64 encoded image
    location: Optional[Dict[str, float]] = None

class DetectionResponse(BaseModel):
    objects: List[Dict]
    location: Optional[Dict]
    total_detected: int
    message: str

@router.post("/yolo", response_model=DetectionResponse)
async def detect_objects_yolo(request: DetectionRequest):
    """
    Real-time object detection using YOLO
    No authentication required for demo
    """
    try:
        logger.info(f"Received detection request with location: {request.location}")
        
        result = yolo_detector.detect_objects(
            image_base64=request.image,
            location=request.location
        )
        
        # Create natural language message
        if result["total_detected"] == 0:
            message = "No objects detected in your path. Area appears clear."
        else:
            obj_list = [f"{obj['label']} at {obj['distance']} on your {obj['position']}" 
                       for obj in result["objects"][:3]]  # Top 3 closest objects
            message = f"I detect {result['total_detected']} objects: " + ", ".join(obj_list)
        
        logger.info(f"Detection complete: {result['total_detected']} objects found")
        
        return {
            **result,
            "message": message
        }
    
    except Exception as e:
        logger.error(f"Detection failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")
