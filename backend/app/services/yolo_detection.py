import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import base64
import io
import math
import logging

logger = logging.getLogger(__name__)

class YOLODetector:
    def __init__(self):
        # Load YOLO model (yolov8n is fastest for real-time detection)
        self.model = YOLO('yolov8n.pt')
        logger.info("YOLO model loaded successfully")
        
    def detect_objects(self, image_base64: str, location: dict = None):
        """
        Detect objects in image using YOLO
        Args:
            image_base64: Base64 encoded image
            location: Dict with latitude/longitude
        Returns:
            List of detected objects with distances and positions
        """
        try:
            # Decode base64 image
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)
            
            # Run YOLO detection
            results = self.model(image_array, verbose=False)[0]
            
            objects = []
            height, width = image_array.shape[:2]
            
            for detection in results.boxes:
                # Get bounding box
                x1, y1, x2, y2 = detection.xyxy[0].tolist()
                confidence = float(detection.conf[0])
                class_id = int(detection.cls[0])
                label = results.names[class_id]
                
                # Only include objects with confidence > 50%
                if confidence < 0.5:
                    continue
                
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
                distance = self._estimate_distance(obj_height, height)
                
                objects.append({
                    "label": label,
                    "confidence": round(confidence * 100, 1),
                    "distance": f"{distance:.1f} meters",
                    "position": position,
                    "bbox": [int(x1), int(y1), int(x2), int(y2)]
                })
            
            # Sort by distance (closest first)
            objects.sort(key=lambda x: float(x['distance'].split()[0]))
            
            return {
                "objects": objects,
                "location": location,
                "total_detected": len(objects)
            }
        
        except Exception as e:
            logger.error(f"Detection error: {str(e)}")
            raise
    
    def _estimate_distance(self, obj_height_pixels, image_height):
        """Estimate distance to object based on pixel height"""
        # Simple estimation: closer objects appear larger
        # This is a rough approximation and should be calibrated for production
        if obj_height_pixels == 0:
            return 10.0
        
        # Assuming FOV of ~60 degrees and average object height of 1.5m
        focal_length = image_height / (2 * math.tan(math.radians(30)))
        distance = (1.5 * focal_length) / obj_height_pixels
        
        # Clamp between 0.5-15 meters
        return max(0.5, min(distance, 15.0))

# Global instance
yolo_detector = YOLODetector()
