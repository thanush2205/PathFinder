"""
AI Detection API Routes
Object detection and navigation assistance
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Dict, List
import cv2
import numpy as np
from io import BytesIO
import base64
from ..models.schemas import DetectionResult, NavigationAlert
from ..core.security import get_current_user
from ..ai_modules.object_detection import object_detector

router = APIRouter(prefix="/ai/detection", tags=["AI Detection"])


@router.on_event("startup")
async def load_detection_model():
    """Load YOLO model on startup"""
    object_detector.load_model()


@router.post("/image", response_model=List[DetectionResult])
async def detect_objects_in_image(
    image: UploadFile = File(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    Detect objects in an uploaded image
    Returns list of detected objects with bounding boxes
    """
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file"
            )
        
        # Detect objects
        detections = object_detector.detect_objects(frame)
        
        return detections
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detection failed: {str(e)}"
        )


@router.post("/image/alert", response_model=NavigationAlert)
async def get_navigation_alert_from_image(
    image: UploadFile = File(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get navigation alert from uploaded image
    Returns prioritized alert for the most dangerous nearby object
    """
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file"
            )
        
        # Detect objects
        detections = object_detector.detect_objects(frame)
        
        # Create navigation alert
        alert = object_detector.create_navigation_alert(detections)
        
        if not alert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hazards detected in image"
            )
        
        return alert
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Alert generation failed: {str(e)}"
        )


@router.post("/image/annotated")
async def get_annotated_image(
    image: UploadFile = File(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    Get image with bounding boxes drawn on detected objects
    Returns annotated image
    """
    try:
        # Read image
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file"
            )
        
        # Process frame with detections
        annotated_frame, _ = object_detector.process_video_frame(frame, draw_boxes=True)
        
        # Encode to JPEG
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        img_bytes = BytesIO(buffer.tobytes())
        
        return StreamingResponse(img_bytes, media_type="image/jpeg")
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image processing failed: {str(e)}"
        )


@router.post("/frame/base64", response_model=List[DetectionResult])
async def detect_objects_in_base64_frame(
    frame_data: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """
    Detect objects in a base64 encoded frame
    Useful for real-time video streaming from mobile app
    
    Expected input: {"frame": "base64_encoded_image_string"}
    """
    try:
        frame_b64 = frame_data.get("frame")
        if not frame_b64:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No frame data provided"
            )
        
        # Decode base64
        img_bytes = base64.b64decode(frame_b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid frame data"
            )
        
        # Detect objects
        detections = object_detector.detect_objects(frame)
        
        return detections
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Detection failed: {str(e)}"
        )


@router.post("/frame/alert", response_model=NavigationAlert)
async def get_navigation_alert_from_frame(
    frame_data: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """
    Get navigation alert from base64 encoded frame
    Real-time alert generation for mobile app
    
    Expected input: {"frame": "base64_encoded_image_string"}
    """
    try:
        frame_b64 = frame_data.get("frame")
        if not frame_b64:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No frame data provided"
            )
        
        # Decode base64
        img_bytes = base64.b64decode(frame_b64)
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid frame data"
            )
        
        # Detect and create alert
        detections = object_detector.detect_objects(frame)
        alert = object_detector.create_navigation_alert(detections)
        
        if not alert:
            # Return a safe alert indicating no hazards
            return NavigationAlert(
                alert_type="clear",
                message="Path is clear",
                severity="low",
                detections=[]
            )
        
        return alert
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Alert generation failed: {str(e)}"
        )


@router.get("/health")
async def detection_health():
    """
    Check if detection model is loaded and ready
    """
    is_ready = object_detector.model is not None
    return {
        "status": "ready" if is_ready else "not_ready",
        "model_loaded": is_ready,
        "confidence_threshold": object_detector.confidence_threshold,
        "target_fps": object_detector.target_fps
    }
