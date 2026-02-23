"""
Demo AI endpoints for testing without heavy ML dependencies
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/ai-demo", tags=["AI Demo"])


class ObjectDetectionDemo(BaseModel):
    objects: List[dict]
    alert: str
    confidence: float


class VoiceCommandDemo(BaseModel):
    command: str
    action: str
    response: str


@router.post("/detect", response_model=ObjectDetectionDemo)
async def demo_object_detection():
    """
    Demo: Shows how object detection works
    In real implementation, this processes camera feed with YOLO
    """
    return {
        "objects": [
            {
                "label": "person",
                "confidence": 0.95,
                "position": "center",
                "distance": "2 meters"
            },
            {
                "label": "chair",
                "confidence": 0.88,
                "position": "left",
                "distance": "1 meter"
            },
            {
                "label": "door",
                "confidence": 0.92,
                "position": "right",
                "distance": "3 meters"
            }
        ],
        "alert": "Person ahead at 2 meters, Chair on left at 1 meter, Door on right at 3 meters",
        "confidence": 0.92
    }


@router.post("/voice", response_model=VoiceCommandDemo)
async def demo_voice_command(command: dict):
    """
    Demo: Shows how voice commands are processed
    In real implementation, this uses speech recognition and TTS
    """
    text = command.get("text", "").lower()
    
    responses = {
        "where am i": {
            "action": "location",
            "response": "You are currently at the main entrance. There's a door 3 meters ahead on your right."
        },
        "what's around me": {
            "action": "scan",
            "response": "I detect a person 2 meters ahead in front of you, a chair on your left at 1 meter, and a door on your right at 3 meters."
        },
        "help me navigate": {
            "action": "navigate",
            "response": "Starting navigation mode. Walk straight for 5 steps. I'll alert you of any obstacles."
        },
        "read text": {
            "action": "ocr",
            "response": "Detecting text in your view. I found: 'Emergency Exit - This Way'. The sign is 2 meters ahead."
        }
    }
    
    # Find matching command
    for key in responses:
        if key in text:
            return {
                "command": text,
                "action": responses[key]["action"],
                "response": responses[key]["response"]
            }
    
    # Default response
    return {
        "command": text,
        "action": "unknown",
        "response": "I can help you with: checking your location, scanning surroundings, navigation, or reading text. What would you like?"
    }


@router.get("/navigation-flow")
async def demo_navigation_flow():
    """
    Demo: Shows the complete AI navigation flow for visually impaired users
    """
    return {
        "flow": [
            {
                "step": 1,
                "feature": "Voice Activation",
                "description": "User says 'Hey PathFinder' to activate the app",
                "ai_response": "Hello! I'm PathFinder, your AI navigation assistant. How can I help you?"
            },
            {
                "step": 2,
                "feature": "Environment Scanning",
                "description": "Camera continuously scans the environment using YOLO v8",
                "ai_detection": "Person ahead (2m), Chair left (1m), Door right (3m)",
                "ai_response": "I'm scanning your surroundings. There's a person 2 meters ahead."
            },
            {
                "step": 3,
                "feature": "Obstacle Alert",
                "description": "AI detects obstacles and provides audio warnings",
                "ai_response": "Warning: Chair detected on your left at 1 meter. Please step to the right."
            },
            {
                "step": 4,
                "feature": "Voice Commands",
                "description": "User can ask questions via voice",
                "user_command": "Where am I?",
                "ai_response": "You are at the main entrance. There's a door 3 meters on your right."
            },
            {
                "step": 5,
                "feature": "Text Recognition (OCR)",
                "description": "AI reads signs and text for the user",
                "user_command": "Read the sign",
                "ai_response": "The sign says: Emergency Exit - This Way. It's 2 meters ahead."
            },
            {
                "step": 6,
                "feature": "Navigation Guidance",
                "description": "Step-by-step navigation with real-time updates",
                "ai_response": "Walk straight for 5 steps. Turn right at the door. I'll guide you through."
            }
        ],
        "technologies": {
            "computer_vision": "YOLO v8 for real-time object detection",
            "speech": "Google Speech Recognition + gTTS for voice interaction",
            "nlp": "Natural language processing for command understanding",
            "ocr": "Optical character recognition for reading text"
        }
    }
