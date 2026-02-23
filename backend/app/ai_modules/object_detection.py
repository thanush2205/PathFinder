"""
Object Detection Module using YOLO
Real-time obstacle and hazard detection
"""
import cv2
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Optional
import logging
from ..models.schemas import DetectionResult, NavigationAlert
from ..core.config import settings

logger = logging.getLogger(__name__)


class ObjectDetector:
    """YOLO-based object detector for navigation assistance"""
    
    def __init__(self):
        """Initialize YOLO model"""
        self.model = None
        self.confidence_threshold = settings.DETECTION_CONFIDENCE
        self.target_fps = settings.DETECTION_FPS
        
        # Hazard classes (COCO dataset classes)
        self.hazard_classes = {
            'person': 'high',
            'bicycle': 'medium',
            'car': 'high',
            'motorcycle': 'high',
            'bus': 'high',
            'truck': 'high',
            'traffic light': 'medium',
            'fire hydrant': 'medium',
            'stop sign': 'high',
            'bench': 'low',
            'chair': 'low',
            'potted plant': 'low',
            'dining table': 'medium',
            'dog': 'medium',
            'cat': 'medium'
        }
    
    def load_model(self):
        """Load YOLO model"""
        try:
            logger.info(f"Loading YOLO model from {settings.YOLO_MODEL_PATH}")
            self.model = YOLO(settings.YOLO_MODEL_PATH)
            logger.info("YOLO model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load YOLO model: {e}")
            # For development, create a dummy model
            logger.warning("Running without YOLO model - using mock detections")
    
    def detect_objects(self, frame: np.ndarray) -> List[DetectionResult]:
        """
        Detect objects in a frame
        
        Args:
            frame: Input image frame (BGR format)
            
        Returns:
            List of detected objects with bounding boxes and confidence
        """
        if self.model is None:
            return self._mock_detection(frame)
        
        try:
            # Run inference
            results = self.model(frame, conf=self.confidence_threshold, verbose=False)
            
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0].cpu().numpy())
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = result.names[class_id]
                    
                    # Calculate distance (rough estimation based on bbox size)
                    distance = self._estimate_distance(x1, y1, x2, y2, frame.shape)
                    
                    # Determine direction
                    direction = self._get_direction(x1, x2, frame.shape[1])
                    
                    detection = DetectionResult(
                        class_name=class_name,
                        confidence=confidence,
                        bbox=[float(x1), float(y1), float(x2), float(y2)],
                        distance=distance,
                        direction=direction
                    )
                    detections.append(detection)
            
            return detections
        
        except Exception as e:
            logger.error(f"Error during detection: {e}")
            return []
    
    def _mock_detection(self, frame: np.ndarray) -> List[DetectionResult]:
        """Mock detection for development without YOLO model"""
        # Return empty list or mock data
        return []
    
    def _estimate_distance(self, x1: float, y1: float, x2: float, y2: float, 
                          frame_shape: Tuple) -> float:
        """
        Estimate distance based on bounding box size
        Larger objects are typically closer
        
        Returns:
            Estimated distance in meters (rough approximation)
        """
        bbox_height = y2 - y1
        frame_height = frame_shape[0]
        
        # Simple inverse relationship - adjust based on calibration
        # This is a very rough approximation
        if bbox_height > 0:
            distance = (frame_height / bbox_height) * 0.5  # Rough scale factor
            return round(distance, 2)
        return 10.0  # Default distance
    
    def _get_direction(self, x1: float, x2: float, frame_width: int) -> str:
        """
        Determine object direction relative to camera center
        
        Returns:
            Direction: 'left', 'center', or 'right'
        """
        center_x = (x1 + x2) / 2
        frame_center = frame_width / 2
        
        threshold = frame_width * 0.2  # 20% threshold
        
        if center_x < frame_center - threshold:
            return 'left'
        elif center_x > frame_center + threshold:
            return 'right'
        else:
            return 'center'
    
    def create_navigation_alert(self, detections: List[DetectionResult]) -> Optional[NavigationAlert]:
        """
        Create navigation alert from detections
        Prioritizes closest and most dangerous objects
        
        Returns:
            NavigationAlert or None if no hazards detected
        """
        if not detections:
            return None
        
        # Filter only hazardous objects
        hazards = [d for d in detections if d.class_name in self.hazard_classes]
        
        if not hazards:
            return None
        
        # Sort by distance (closest first)
        hazards.sort(key=lambda x: x.distance if x.distance else 100)
        
        closest_hazard = hazards[0]
        severity = self.hazard_classes.get(closest_hazard.class_name, 'low')
        
        # Create alert message
        direction_text = closest_hazard.direction
        distance_text = f"{closest_hazard.distance:.1f} meters" if closest_hazard.distance else "nearby"
        
        message = f"{closest_hazard.class_name.capitalize()} detected {direction_text}, approximately {distance_text} away"
        
        alert = NavigationAlert(
            alert_type=closest_hazard.class_name,
            message=message,
            severity=severity,
            detections=hazards[:3]  # Include top 3 hazards
        )
        
        return alert
    
    def process_video_frame(self, frame: np.ndarray, draw_boxes: bool = True) -> Tuple[np.ndarray, Optional[NavigationAlert]]:
        """
        Process a single video frame with detection and alert generation
        
        Args:
            frame: Input frame
            draw_boxes: Whether to draw bounding boxes on frame
            
        Returns:
            Tuple of (processed frame, navigation alert)
        """
        # Detect objects
        detections = self.detect_objects(frame)
        
        # Draw bounding boxes if requested
        if draw_boxes and detections:
            frame = self._draw_detections(frame, detections)
        
        # Create navigation alert
        alert = self.create_navigation_alert(detections)
        
        return frame, alert
    
    def _draw_detections(self, frame: np.ndarray, detections: List[DetectionResult]) -> np.ndarray:
        """Draw bounding boxes on frame"""
        for detection in detections:
            x1, y1, x2, y2 = map(int, detection.bbox)
            
            # Color based on severity
            severity = self.hazard_classes.get(detection.class_name, 'low')
            if severity == 'high':
                color = (0, 0, 255)  # Red
            elif severity == 'medium':
                color = (0, 165, 255)  # Orange
            else:
                color = (0, 255, 0)  # Green
            
            # Draw box
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            
            # Draw label
            label = f"{detection.class_name} {detection.confidence:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        return frame


# Global detector instance
object_detector = ObjectDetector()
