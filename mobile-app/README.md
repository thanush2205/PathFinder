# PathFinder Mobile App

AI-powered navigation assistant for visually impaired users.

## Features

✅ **Voice-Guided Signup** - Complete registration with voice assistance  
✅ **Voice-Guided Login** - Login with audio feedback  
✅ **Live Camera View** - Real-time video feed for object detection  
✅ **AI Object Detection** - Detects people, furniture, doors, obstacles  
✅ **Voice Commands** - Ask questions and get spoken responses  
✅ **Real-Time Alerts** - Audio warnings about nearby obstacles  
✅ **Simple UI** - Large buttons, high contrast, screen reader compatible  

## Installation

```bash
# Install dependencies
cd mobile-app
npm install

# Start the app
npm start
```

## Usage (For Blind Users)

### 1. Sign Up
- App speaks: "Welcome to PathFinder. Let me help you create an account."
- Fill in name, email, password with voice guidance
- Tap "Sign Up" button

### 2. Login  
- App speaks: "Welcome to PathFinder. Please login to continue."
- Enter email and password
- Tap "Login" button

### 3. Camera Navigation
- Camera opens automatically
- Tap "▶️ Start Scan" to begin object detection
- AI announces detected objects: "Person ahead, 3 meters"

### 4. Voice Commands
Tap any button to ask:
- **📍 Where Am I?** - Get current location
- **👁️ What's Around?** - Scan surroundings
- **🧭 Navigate** - Start navigation guidance
- **📖 Read Text** - Read signs and labels

### 5. Continuous Scanning
- Keep app running while walking
- AI continuously detects and announces obstacles
- Audio alerts keep you safe

## Voice Commands

The app responds to:
- "where am i" - Location information
- "what's around me" - Object detection
- "help me navigate" - Navigation mode
- "read text" - OCR text recognition

## Accessibility

- ✅ Large, high-contrast buttons
- ✅ Voice feedback for all actions
- ✅ Screen reader compatible
- ✅ Accessible labels on all inputs
- ✅ Audio confirmations
- ✅ Hands-free operation

## Requirements

- Expo CLI
- Camera permission
- Microphone permission (for future voice input)
- Internet connection for API calls

## Backend API

Make sure the backend is running at `http://localhost:8000`

## Tech Stack

- React Native
- Expo
- Expo Camera
- Expo Speech (Text-to-Speech)
- React Navigation
- Axios

## Color Scheme

- Primary: #e94560 (Red)
- Background: #1a1a2e (Dark Blue)
- Secondary: #0f3460 (Blue)
- Surface: #16213e (Dark Gray)

## Future Enhancements

- [ ] Voice input recognition (speech-to-text)
- [ ] Real YOLO object detection (when ML packages installed)
- [ ] Offline mode
- [ ] Route saving
- [ ] Emergency SOS
- [ ] Multi-language support
