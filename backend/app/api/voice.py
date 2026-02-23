"""
Voice Assistant API Routes
Speech-to-text and text-to-speech functionality
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import FileResponse, Response
from typing import Dict
import base64
from pathlib import Path
import tempfile
import os
from ..models.schemas import VoiceCommand, VoiceResponse
from ..core.security import get_current_user
from ..ai_modules.voice_assistant import voice_assistant

router = APIRouter(prefix="/ai/voice", tags=["Voice Assistant"])


@router.post("/speech-to-text")
async def convert_speech_to_text(
    audio: UploadFile = File(...),
    current_user: Dict = Depends(get_current_user)
):
    """
    Convert uploaded audio file to text
    Supports WAV, MP3, FLAC formats
    """
    try:
        # Save audio temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio.filename).suffix) as temp_file:
            contents = await audio.read()
            temp_file.write(contents)
            temp_path = temp_file.name
        
        # Convert speech to text
        text = voice_assistant.speech_to_text(audio_file=temp_path)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not understand audio"
            )
        
        return {"text": text}
    
    except HTTPException:
        raise
    except Exception as e:
        # Clean up temp file on error
        if 'temp_path' in locals():
            try:
                os.unlink(temp_path)
            except:
                pass
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Speech recognition failed: {str(e)}"
        )


@router.post("/text-to-speech")
async def convert_text_to_speech(
    data: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """
    Convert text to speech
    Returns base64 encoded audio
    
    Expected input: {"text": "Text to convert to speech"}
    """
    try:
        text = data.get("text")
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text provided"
            )
        
        # Convert text to speech
        audio_base64 = voice_assistant.text_to_speech(text)
        
        if not audio_base64:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate speech"
            )
        
        return {
            "audio": audio_base64,
            "format": "mp3",
            "encoding": "base64"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text-to-speech failed: {str(e)}"
        )


@router.post("/text-to-speech/file")
async def convert_text_to_speech_file(
    data: Dict,
    current_user: Dict = Depends(get_current_user)
):
    """
    Convert text to speech and return audio file
    
    Expected input: {"text": "Text to convert to speech"}
    """
    try:
        text = data.get("text")
        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No text provided"
            )
        
        # Create temp file for audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_path = temp_file.name
        
        # Convert text to speech and save
        audio_path = voice_assistant.text_to_speech(text, save_path=temp_path)
        
        if not audio_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate speech"
            )
        
        return FileResponse(
            audio_path,
            media_type="audio/mpeg",
            filename="speech.mp3"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text-to-speech failed: {str(e)}"
        )


@router.post("/process-command", response_model=VoiceResponse)
async def process_voice_command(
    command: VoiceCommand,
    current_user: Dict = Depends(get_current_user)
):
    """
    Process a voice command and generate appropriate response
    Handles both audio and text input
    """
    try:
        response = voice_assistant.process_voice_command(command)
        return response
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Command processing failed: {str(e)}"
        )


@router.post("/guided-signup")
async def start_guided_signup():
    """
    Start voice-guided signup flow
    Returns first question for user
    """
    try:
        text = "Welcome to PathFinder. Let's create your account. What is your name?"
        audio = voice_assistant.text_to_speech(text)
        
        return {
            "text": text,
            "audio": audio,
            "step": "name",
            "next_step": "email"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Guided signup failed: {str(e)}"
        )


@router.post("/role-selection")
async def role_selection():
    """
    Voice-based role selection prompt
    """
    try:
        text = "Welcome to PathFinder. Are you a User or an Admin?"
        audio = voice_assistant.text_to_speech(text)
        
        return {
            "text": text,
            "audio": audio,
            "options": ["user", "admin"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Role selection failed: {str(e)}"
        )


@router.get("/health")
async def voice_health():
    """
    Check voice assistant health status
    """
    return {
        "status": "ready",
        "tts_engine": voice_assistant.tts_engine,
        "language": voice_assistant.language,
        "recognizer_available": voice_assistant.recognizer is not None
    }
