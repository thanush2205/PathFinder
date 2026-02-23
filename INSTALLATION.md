# PathFinder AI - Complete Installation Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Backend Setup](#backend-setup)
4. [Mobile App Setup](#mobile-app-setup)
5. [Admin Dashboard Setup](#admin-dashboard-setup)
6. [Firebase Configuration](#firebase-configuration)
7. [Running the Application](#running-the-application)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

#### 1. **Python 3.12+**
```bash
# Check Python version
python3 --version

# Install Python (Ubuntu/Debian)
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip

# Install Python (macOS with Homebrew)
brew install python@3.12

# Install Python (Windows)
# Download from https://www.python.org/downloads/
```

#### 2. **Node.js 18+ and npm**
```bash
# Check Node.js version
node --version
npm --version

# Install Node.js (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Node.js (macOS with Homebrew)
brew install node@18

# Install Node.js (Windows)
# Download from https://nodejs.org/
```

#### 3. **Git**
```bash
# Check Git version
git --version

# Install Git (Ubuntu/Debian)
sudo apt install git

# Install Git (macOS)
brew install git

# Install Git (Windows)
# Download from https://git-scm.com/
```

#### 4. **Expo CLI**
```bash
# Install Expo CLI globally
npm install -g expo-cli

# Or use npx (no global installation needed)
npx expo --version
```

#### 5. **Expo Go App** (Mobile Device)
- **Android**: Download from [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)
- **iOS**: Download from [App Store](https://apps.apple.com/app/expo-go/id982107779)
- **Required Version**: SDK 54+

---

## System Requirements

### Backend Server
- **OS**: Linux, macOS, or Windows
- **RAM**: Minimum 4GB (8GB recommended for YOLO)
- **Storage**: 2GB free space
- **CPU**: Multi-core processor (GPU optional for faster YOLO inference)

### Development Machine
- **OS**: Linux, macOS, or Windows
- **RAM**: Minimum 8GB
- **Storage**: 5GB free space
- **Network**: WiFi connection (for mobile app testing)

### Mobile Device
- **Android**: Version 10+ with Expo Go (SDK 54)
- **iOS**: Version 13+ with Expo Go (SDK 54)
- **Camera**: Required for object detection
- **GPS**: Required for location tracking

---

## Backend Setup

### 1. Clone Repository
```bash
cd ~/Desktop
git clone <repository-url> pathFinder
cd pathFinder/PathFinder
```

### 2. Create Python Virtual Environment
```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
# Ensure virtual environment is activated
pip install --upgrade pip

# Install all backend dependencies
pip install -r requirements.txt

# Key packages installed:
# - fastapi: Web framework
# - uvicorn: ASGI server
# - firebase-admin: Firebase integration
# - ultralytics: YOLO object detection
# - torch, torchvision: Deep learning
# - opencv-python-headless: Computer vision
# - pillow: Image processing
# - python-multipart: File uploads
# - pydantic: Data validation
```

### 4. Download YOLO Model
```bash
# The YOLOv8n model will auto-download on first run
# Or manually download:
python3 -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); print('Model downloaded')"
```

### 5. Configure Firebase
```bash
# Copy environment template
cp ../.env.example ../.env

# Edit .env file with your Firebase credentials
nano ../.env
```

Add your Firebase configuration:
```env
# Firebase Configuration
FIREBASE_PROJECT_ID=pathfinder-4e3ff
FIREBASE_DATABASE_URL=https://pathfinder-4e3ff-default-rtdb.firebaseio.com/
FIREBASE_STORAGE_BUCKET=pathfinder-4e3ff.appspot.com

# Backend Configuration
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# YOLO Configuration
YOLO_MODEL_PATH=yolov8n.pt
YOLO_CONFIDENCE_THRESHOLD=0.5
```

### 6. Place Firebase Service Account Key
```bash
# Copy your Firebase service account JSON file to project root
# The file should be named: pathfinder-4e3ff-firebase-adminsdk-*.json
# Location: /pathFinder/PathFinder/pathfinder-4e3ff-firebase-adminsdk-*.json
```

### 7. Verify Installation
```bash
# Test Python imports
python3 -c "import fastapi, firebase_admin, ultralytics, cv2; print('All imports successful')"

# Test YOLO model
python3 -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); print('YOLO ready')"
```

---

## Mobile App Setup

### 1. Navigate to Mobile App Directory
```bash
cd ../mobile-app
```

### 2. Install Node.js Dependencies
```bash
# Install all npm packages
npm install

# Key packages installed:
# - expo: SDK 54
# - react-native: 0.81.5
# - react: 19.1.0
# - expo-camera: Camera API
# - expo-location: GPS tracking
# - expo-speech: Text-to-speech
# - expo-av: Audio recording
# - @react-navigation/native: Navigation
```

### 3. Configure Backend API URL
```bash
# Open CameraNavigationScreen.js
nano src/screens/CameraNavigationScreen.js
```

Update the API URL (line 16):
```javascript
const API_URL = 'http://YOUR_LAPTOP_IP:8000/api';
```

Find your laptop IP:
```bash
# Linux/macOS
ip addr show | grep "inet " | grep -v 127.0.0.1

# Windows
ipconfig | findstr IPv4
```

### 4. Verify Expo Installation
```bash
# Check Expo version
npx expo --version

# Should show SDK 54+
```

---

## Admin Dashboard Setup

### 1. Navigate to Admin Dashboard Directory
```bash
cd ../admin-dashboard
```

### 2. Install Dependencies
```bash
npm install

# Key packages installed:
# - react: 18+
# - react-router-dom: Routing
# - axios: HTTP client
# - firebase: Firebase SDK
```

### 3. Configure Firebase
```bash
# Create .env file
nano .env
```

Add Firebase configuration:
```env
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=pathfinder-4e3ff.firebaseapp.com
REACT_APP_FIREBASE_DATABASE_URL=https://pathfinder-4e3ff-default-rtdb.firebaseio.com/
REACT_APP_FIREBASE_PROJECT_ID=pathfinder-4e3ff
REACT_APP_FIREBASE_STORAGE_BUCKET=pathfinder-4e3ff.appspot.com
REACT_APP_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
REACT_APP_FIREBASE_APP_ID=your_app_id
REACT_APP_API_URL=http://localhost:8000/api
```

---

## Firebase Configuration

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Enter project name: `pathfinder-4e3ff`
4. Enable Google Analytics (optional)
5. Create project

### 2. Enable Realtime Database
1. In Firebase Console, go to "Realtime Database"
2. Click "Create Database"
3. Choose location (closest to your users)
4. Start in **test mode** (or use provided rules)
5. Copy database URL

### 3. Generate Service Account Key
1. Go to Project Settings → Service Accounts
2. Click "Generate New Private Key"
3. Download JSON file
4. Rename to `pathfinder-4e3ff-firebase-adminsdk-*.json`
5. Place in project root directory

### 4. Configure Database Rules
```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null",
    "users": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid"
      }
    },
    "detections": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

---

## Running the Application

### 1. Start Backend Server

```bash
cd backend

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows

# Start backend server
python3 run.py

# Server will start on http://0.0.0.0:8000
# API docs available at http://localhost:8000/docs
```

**Expected Output:**
```
INFO:     Starting PathFinder API
INFO:     Firebase initialized successfully
INFO:     API server started on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Start Mobile App

Open a new terminal:
```bash
cd mobile-app

# Start Expo development server
npx expo start

# Options:
# --lan    : Use local network (recommended)
# --tunnel : Use ngrok tunnel (if on different networks)
# --localhost : Use localhost only
```

**Expected Output:**
```
Starting Metro Bundler
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
█ ▄▄▄▄▄ █  QR CODE   █
█ █   █ █             █
█ █▄▄▄█ █             █
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

› Metro waiting on exp://YOUR_IP:8081
› Scan the QR code above with Expo Go
```

### 3. Run Mobile App on Device

1. **Open Expo Go** app on your phone
2. **Scan QR code** from terminal
3. **Wait for app to load** (may take 1-2 minutes first time)
4. **Grant permissions**:
   - Camera access
   - Location access
   - Microphone access

### 4. Start Admin Dashboard (Optional)

Open a new terminal:
```bash
cd admin-dashboard

# Start development server
npm start

# Dashboard will open at http://localhost:3000
```

---

## Testing the Application

### 1. Test Backend API
```bash
# Health check
curl http://localhost:8000/

# API documentation
curl http://localhost:8000/docs

# Test YOLO endpoint (requires base64 image)
curl -X POST http://localhost:8000/api/detection/yolo \
  -H "Content-Type: application/json" \
  -d '{"image":"<base64_string>","location":{"latitude":37.7749,"longitude":-122.4194}}'
```

### 2. Test Mobile App
1. Point camera at common objects (chair, table, door, person, cup, phone)
2. App automatically scans every 3 seconds
3. Listen for voice announcements: *"I detect 2 objects: Chair at 2.5 meters on your left..."*
4. Tap microphone button to test voice commands (demo mode)

### 3. Monitor Backend Logs
```bash
# In backend terminal, watch for:
# - Incoming detection requests
# - YOLO inference times
# - Detected objects
# - Any errors
```

---

## Troubleshooting

### Backend Issues

#### Issue: `ModuleNotFoundError: No module named 'fastapi'`
**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: `YOLO model not found`
**Solution:**
```bash
# Download model manually
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

#### Issue: `Firebase permission denied`
**Solution:**
- Check Firebase service account JSON file is in correct location
- Verify FIREBASE_DATABASE_URL in .env file
- Check Firebase database rules

### Mobile App Issues

#### Issue: `Network request failed`
**Solution:**
1. Ensure phone and laptop are on **same WiFi network**
2. Check backend is running: `curl http://YOUR_IP:8000/`
3. Update API_URL in CameraNavigationScreen.js with correct IP
4. Try tunnel mode: `npx expo start --tunnel`

#### Issue: `Expo SDK version mismatch`
**Solution:**
```bash
# Update Expo Go app on phone to SDK 54+
# Or downgrade project to match your Expo Go version
npx expo upgrade
```

#### Issue: `Camera permission denied`
**Solution:**
1. Go to phone Settings → Apps → Expo Go
2. Enable Camera, Location, and Microphone permissions
3. Restart Expo Go app

### Node.js Compatibility Issues

#### Issue: `os.availableParallelism is not a function`
**Solution:**
Already handled with polyfills in `metro-polyfill.js`

#### Issue: `Array.toReversed is not a function`
**Solution:**
Already handled with polyfills in `metro-polyfill.js`

### Performance Issues

#### Issue: YOLO detection is slow (>5 seconds)
**Solutions:**
1. Use GPU-enabled backend server
2. Reduce image quality in mobile app (change `quality: 0.5` to `0.3`)
3. Increase scan interval (change `3000ms` to `5000ms`)
4. Use YOLOv8n-tiny model (smaller, faster)

---

## Project Structure

```
PathFinder/
├── backend/                    # FastAPI backend server
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── ai_demo.py
│   │   │   └── yolo_detection.py
│   │   ├── services/          # Business logic
│   │   │   ├── database.py    # Firebase integration
│   │   │   └── yolo_detection.py  # YOLO service
│   │   └── main.py            # FastAPI app
│   ├── run.py                 # Entry point
│   ├── requirements.txt       # Python dependencies
│   └── venv/                  # Virtual environment
│
├── mobile-app/                # React Native Expo app
│   ├── src/
│   │   ├── screens/
│   │   │   └── CameraNavigationScreen.js  # Main camera screen
│   │   ├── navigation/
│   │   └── components/
│   ├── App.js                 # App entry point
│   ├── package.json           # npm dependencies
│   ├── metro.config.js        # Metro bundler config
│   └── metro-polyfill.js      # Node.js polyfills
│
├── admin-dashboard/           # React admin dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.js
│   └── package.json
│
├── .env                       # Environment variables
├── .env.example              # Environment template
├── firebase-database-rules.json  # Firebase rules
├── pathfinder-*-adminsdk-*.json  # Firebase service account
└── INSTALLATION.md           # This file
```

---

## Quick Start Summary

```bash
# 1. Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py

# 2. Mobile App (new terminal)
cd mobile-app
npm install
npx expo start --lan

# 3. Scan QR code with Expo Go app on your phone
# 4. Grant camera, location, and microphone permissions
# 5. Point camera at objects - automatic detection starts!
```

---

## Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **YOLO Documentation**: https://docs.ultralytics.com/
- **Expo Documentation**: https://docs.expo.dev/
- **Firebase Documentation**: https://firebase.google.com/docs
- **React Native Documentation**: https://reactnative.dev/

---

## Support

For issues and questions:
1. Check this INSTALLATION.md file
2. Review TESTING_GUIDE.md for testing procedures
3. Check YOLO_INTEGRATION_GUIDE.md for AI model details
4. Review backend logs: `backend/backend.log`
5. Check Expo terminal for mobile app errors

---

## License

[Your License Here]

---

## Contributors

[Your Name/Team]

Last Updated: February 23, 2026
