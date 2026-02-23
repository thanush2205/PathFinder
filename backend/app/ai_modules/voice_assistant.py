"""
Voice Assistant Module
Speech-to-Text and Text-to-Speech functionality
"""
import speech_recognition as sr
from gtts import gTTS
import pyttsx3
import logging
from typing import Optional, Dict, Any
import io
import base64
from ..core.config import settings
from ..models.schemas import VoiceCommand, VoiceResponse

logger = logging.getLogger(__name__)


class VoiceAssistant:
    """AI Voice Assistant for PathFinder"""
    
    def __init__(self):
        """Initialize voice assistant"""
        self.recognizer = sr.Recognizer()
        self.tts_engine = settings.TTS_ENGINE
        self.language = settings.STT_LANGUAGE
        
        # Initialize pyttsx3 if using local TTS
        if self.tts_engine == "pyttsx3":
            try:
                self.pyttsx3_engine = pyttsx3.init()
                self.pyttsx3_engine.setProperty('rate', 150)  # Speed
                self.pyttsx3_engine.setProperty('volume', 0.9)  # Volume
            except Exception as e:
                logger.error(f"Failed to initialize pyttsx3: {e}")
                self.pyttsx3_engine = None
    
    def speech_to_text(self, audio_data: Optional[bytes] = None, 
                       audio_file: Optional[str] = None) -> Optional[str]:
        """
        Convert speech to text
        
        Args:
            audio_data: Raw audio bytes
            audio_file: Path to audio file
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            if audio_file:
                with sr.AudioFile(audio_file) as source:
                    audio = self.recognizer.record(source)
            elif audio_data:
                # Convert bytes to AudioData
                audio = sr.AudioData(audio_data, 16000, 2)
            else:
                logger.error("No audio data provided")
                return None
            
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"Recognized speech: {text}")
            return text
            
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in speech recognition: {e}")
            return None
    
    def text_to_speech(self, text: str, save_path: Optional[str] = None) -> Optional[str]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            save_path: Optional path to save audio file
            
        Returns:
            Base64 encoded audio or file path
        """
        try:
            if self.tts_engine == "gtts":
                # Use Google Text-to-Speech
                tts = gTTS(text=text, lang='en', slow=False)
                
                if save_path:
                    tts.save(save_path)
                    return save_path
                else:
                    # Return base64 encoded audio
                    audio_buffer = io.BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    audio_base64 = base64.b64encode(audio_buffer.read()).decode()
                    return audio_base64
            
            elif self.tts_engine == "pyttsx3" and self.pyttsx3_engine:
                # Use local pyttsx3
                if save_path:
                    self.pyttsx3_engine.save_to_file(text, save_path)
                    self.pyttsx3_engine.runAndWait()
                    return save_path
                else:
                    # pyttsx3 doesn't support in-memory generation easily
                    logger.warning("pyttsx3 requires save_path")
                    return None
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return None
    
    def listen_microphone(self, timeout: int = 5) -> Optional[str]:
        """
        Listen to microphone and convert to text
        
        Args:
            timeout: Maximum time to listen
            
        Returns:
            Transcribed text or None
        """
        try:
            with sr.Microphone() as source:
                logger.info("Listening...")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with timeout
                audio = self.recognizer.listen(source, timeout=timeout, 
                                              phrase_time_limit=timeout)
                
                # Convert to text
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"Heard: {text}")
                return text
                
        except sr.WaitTimeoutError:
            logger.warning("Listening timeout")
            return None
        except Exception as e:
            logger.error(f"Microphone error: {e}")
            return None
    
    def process_voice_command(self, command: VoiceCommand) -> VoiceResponse:
        """
        Process a voice command and generate response
        
        Args:
            command: Voice command with audio or text
            
        Returns:
            Voice response with text and optional audio
        """
        # Get text from audio if provided
        if command.audio_data and not command.text:
            audio_bytes = base64.b64decode(command.audio_data)
            command.text = self.speech_to_text(audio_data=audio_bytes)
        
        if not command.text:
            return VoiceResponse(
                text="I didn't understand that. Please try again.",
                action="error"
            )
        
        # Process the command (basic implementation)
        text_lower = command.text.lower()
        
        # Simple command recognition
        response_text = ""
        action = None
        data = None
        
        if any(word in text_lower for word in ["help", "assist", "guide"]):
            response_text = "I'm here to help you navigate safely. You can ask me to start navigation, submit a complaint, or get assistance."
            action = "help"
        
        elif any(word in text_lower for word in ["navigate", "start", "begin"]):
            response_text = "Starting navigation. I'll alert you about obstacles and hazards ahead."
            action = "start_navigation"
        
        elif any(word in text_lower for word in ["stop", "end", "finish"]):
            response_text = "Navigation stopped. Stay safe!"
            action = "stop_navigation"
        
        elif any(word in text_lower for word in ["complaint", "problem", "issue"]):
            response_text = "I'm listening. Please describe your complaint or issue."
            action = "complaint"
        
        else:
            response_text = f"I heard: {command.text}. How can I help you?"
            action = "unknown"
            data = {"original_text": command.text}
        
        # Generate audio response
        audio_url = self.text_to_speech(response_text)
        
        return VoiceResponse(
            text=response_text,
            audio_url=audio_url,
            action=action,
            data=data
        )
    
    def guided_signup(self) -> Dict[str, Any]:
        """
        Guided voice-based signup flow
        
        Returns:
            User data collected through voice
        """
        user_data = {}
        
        # Ask for name
        name_response = self.text_to_speech("Welcome to PathFinder. What is your name?")
        # In production, this would wait for user response
        # user_data['name'] = self.listen_microphone()
        
        # Ask for email
        email_response = self.text_to_speech("What is your email address?")
        # user_data['email'] = self.listen_microphone()
        
        # Ask for password preference
        password_response = self.text_to_speech(
            "Would you like me to auto-generate a secure password, or would you prefer to speak your own password?"
        )
        # choice = self.listen_microphone()
        
        return user_data
    
    def role_selection(self) -> Optional[str]:
        """
        Voice-based role selection (User or Admin)
        
        Returns:
            Role: 'user' or 'admin'
        """
        self.text_to_speech("Welcome to PathFinder. Are you a User or an Admin?")
        
        # In production, listen for response
        # response = self.listen_microphone()
        # if response and 'admin' in response.lower():
        #     return 'admin'
        # else:
        #     return 'user'
        
        return 'user'  # Default


# Global voice assistant instance
voice_assistant = VoiceAssistant()
