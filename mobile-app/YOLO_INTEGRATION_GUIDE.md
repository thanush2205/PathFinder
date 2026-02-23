# PathFinder - Real AI Integration Guide

## Overview
This guide explains how to integrate real YOLO object detection, GPS location, and voice input for blind users.

## Backend Setup (YOLO Object Detection)

### 1. Install Required Packages

```bash
cd /home/thanush/Desktop/pathFinder/PathFinder/backend
pip install ultralytics opencv-python-headless torch torchvision pillow numpy
```

### 2. Create YOLO Detection Service

Create file: `backend/app/services/yolo_detection.py`

```python
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import base64
import io
import math

class YOLODetector:
    def __init__(self):
        # Load YOLO model (yolov8n is fastest, yolov8x is most accurate)
        self.model = YOLO('yolov8n.pt')  # Downloads automatically on first run
        
    def detect_objects(self, image_base64: str, location: dict = None):
        """
        Detect objects in image using YOLO
        Args:
            image_base64: Base64 encoded image
            location: Dict with latitude/longitude
        Returns:
            List of detected objects with distances and positions
        """
        # Decode base64 image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        
        # Run YOLO detection
        results = self.model(image_array)[0]
        
        objects = []
        height, width = image_array.shape[:2]
        
        for detection in results.boxes:
            # Get bounding box
            x1, y1, x2, y2 = detection.xyxy[0].tolist()
            confidence = float(detection.conf[0])
            class_id = int(detection.cls[0])
            label = results.names[class_id]
            
            # Calculate position (left/center/right)
            center_x = (x1 + x2) / 2
            if center_x < width / 3:
                position = "left"
            elif center_x < 2 * width / 3:
                position = "center"
            else:
                position = "right"
            
            # Estimate distance based on object size (rough approximation)
            obj_height = y2 - y1
            # Assuming average object height of 1.5m and camera FOV
            distance = self._estimate_distance(obj_height, height)
            
            objects.append({
                "label": label,
                "confidence": round(confidence * 100, 1),
                "distance": f"{distance:.1f} meters",
                "position": position,
                "bbox": [int(x1), int(y1), int(x2), int(y2)]
            })
        
        return {
            "objects": objects,
            "location": location,
            "total_detected": len(objects)
        }
    
    def _estimate_distance(self, obj_height_pixels, image_height):
        """Estimate distance to object based on pixel height"""
        # Simple estimation: closer objects appear larger
        # This is a rough approximation and should be calibrated
        if obj_height_pixels == 0:
            return 10.0
        
        # Assuming FOV of ~60 degrees and average object height of 1.5m
        focal_length = image_height / (2 * math.tan(math.radians(30)))
        distance = (1.5 * focal_length) / obj_height_pixels
        
        return max(0.5, min(distance, 15.0))  # Clamp between 0.5-15 meters

yolo_detector = YOLODetector()
```

### 3. Create YOLO API Endpoint

Create file: `backend/app/api/yolo_detection.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from ..services.yolo_detection import yolo_detector
from ..core.auth import get_current_user

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
async def detect_objects_yolo(
    request: DetectionRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Real-time object detection using YOLO
    """
    try:
        result = yolo_detector.detect_objects(
            image_base64=request.image,
            location=request.location
        )
        
        # Create natural language message
        if result["total_detected"] == 0:
            message = "No objects detected in your path. Area appears clear."
        else:
            obj_list = [f"{obj['label']} at {obj['distance']} on your {obj['position']}" 
                       for obj in result["objects"][:3]]  # Top 3 objects
            message = f"I detect {result['total_detected']} objects: " + ", ".join(obj_list)
        
        return {
            **result,
            "message": message
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")
```

### 4. Register YOLO Router

Update `backend/app/api/__init__.py`:

```python
from fastapi import APIRouter
from .auth import router as auth_router
from .ai_demo import router as ai_demo_router
from .yolo_detection import router as yolo_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(ai_demo_router, prefix="/ai-demo", tags=["ai-demo"])
api_router.include_router(yolo_router, prefix="/detection", tags=["yolo-detection"])
```

## Mobile App - Voice Input Integration

### Install Speech Recognition Package

For voice input, you'll need to integrate with a speech-to-text service:

**Option 1: Google Cloud Speech-to-Text**
```bash
npm install @google-cloud/speech --legacy-peer-deps
```

**Option 2: Expo Speech Recognition (Coming Soon)**
Wait for official expo-speech-recognition package

**Option 3: Web Speech API (React Native)**
```bash
npm install react-native-voice --legacy-peer-deps
```

### Update Mobile App for Continuous Listening

The mobile app code has been updated to:
- ✅ Continuously listen for voice commands
- ✅ Capture camera frames every 2 seconds
- ✅ Send images to YOLO backend
- ✅ Get GPS location
- ✅ Speak detection results

## Testing the Integration

### 1. Start Backend with YOLO
```bash
cd /home/thanush/Desktop/pathFinder/PathFinder/backend
python3 run.py
```

### 2. Test YOLO Endpoint
```bash
curl -X POST http://localhost:8000/api/detection/yolo \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "image": "BASE64_IMAGE_DATA",
    "location": {"latitude": 37.7749, "longitude": -122.4194}
  }'
```

### 3. Start Mobile App
```bash
cd /home/thanush/Desktop/pathFinder/PathFinder/mobile-app
npx expo start --tunnel
```

## Performance Optimization

### For Real-Time Detection:
1. **Use YOLOv8n** (nano) - fastest model
2. **Reduce image quality** to 0.3-0.5
3. **Increase detection interval** to 3-5 seconds
4. **Filter low confidence detections** (< 50%)

### For Better Accuracy:
1. **Use YOLOv8x** (extra large) - most accurate
2. **Use full image quality** (0.8-1.0)
3. **Consider using GPU** on backend
4. **Fine-tune distance estimation** with real-world calibration

## Voice Command Integration

For production, integrate with:
- **Google Cloud Speech-to-Text**: Most accurate, supports 120+ languages
- **Azure Speech Services**: Good alternative with real-time streaming
- **Amazon Transcribe**: AWS-based solution

## Next Steps

1. Install YOLO dependencies on backend
2. Create yolo_detection.py service
3. Test YOLO endpoint with sample images
4. Integrate voice recognition service
5. Deploy backend with GPU for better performance
6. Add offline caching for common objects
7. Implement navigation pathfinding algorithm

## Cost Considerations

- **Google Cloud Speech-to-Text**: $0.006 per 15 seconds
- **YOLO Model**: Free, runs on your server
- **GPS**: Free (device built-in)
- **Expo Go**: Free for development

For production, consider:
- Cloud GPU instances (~$0.50/hour)
- Speech-to-Text API costs
- Backend hosting costs
