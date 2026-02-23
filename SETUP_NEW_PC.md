# 🚀 PathFinder AI - Complete Setup Guide for New PCs

## 📋 Pre-Installation Checklist

Before you begin, ensure you have:
- [ ] A computer running Linux, macOS, or Windows
- [ ] Stable internet connection (for downloading dependencies)
- [ ] At least 5GB free disk space
- [ ] Administrator/sudo privileges
- [ ] A smartphone with Expo Go app installed

---

## 1️⃣ Install Required Software

### Step 1: Install Python 3.12+

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
python3 --version  # Should show 3.12.x
```

#### macOS (with Homebrew):
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.12
python3 --version
```

#### Windows:
1. Download from https://www.python.org/downloads/
2. Run installer, check "Add Python to PATH"
3. Verify: Open CMD and type `python --version`

---

### Step 2: Install Node.js 18+ and npm

#### Linux (Ubuntu/Debian):
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
node --version  # Should show v18.x.x
npm --version
```

#### macOS (with Homebrew):
```bash
brew install node@18
node --version
npm --version
```

#### Windows:
1. Download from https://nodejs.org/
2. Run installer
3. Verify: Open CMD and type `node --version`

---

### Step 3: Install Git

#### Linux:
```bash
sudo apt install git
git --version
```

#### macOS:
```bash
brew install git
git --version
```

#### Windows:
1. Download from https://git-scm.com/
2. Run installer
3. Verify: Open CMD and type `git --version`

---

### Step 4: Install Expo Go on Your Phone

- **Android**: https://play.google.com/store/apps/details?id=host.exp.exponent
- **iOS**: https://apps.apple.com/app/expo-go/id982107779

**Important**: Must be SDK 54 or higher!

---

## 2️⃣ Clone and Setup Project

### Step 1: Clone Repository
```bash
cd ~/Desktop  # or any directory you prefer
git clone <repository-url> pathFinder
cd pathFinder/PathFinder
```

---

## 3️⃣ Backend Setup

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# Create venv
python3 -m venv venv

# Activate venv
# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Your prompt should now show (venv)
```

### Step 3: Install Python Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install all backend packages
pip install -r requirements.txt

# This will install:
# - fastapi (web framework)
# - uvicorn (server)
# - firebase-admin (database)
# - ultralytics (YOLO AI model)
# - torch, torchvision (deep learning)
# - opencv-python-headless (computer vision)
# - pillow (image processing)
# - and more...
```

**Note**: This may take 5-10 minutes depending on your internet speed.

### Step 4: Download YOLO Model
```bash
# Test YOLO installation and download model
python3 -c "from ultralytics import YOLO; model = YOLO('yolov8n.pt'); print('✅ YOLO ready!')"

# Should output: "✅ YOLO ready!"
```

---

## 4️⃣ Firebase Configuration

### Step 1: Create Firebase Project
1. Go to https://console.firebase.google.com/
2. Click "Add Project"
3. Enter name: `pathfinder-4e3ff` (or your choice)
4. Disable Google Analytics (or enable if you want)
5. Click "Create Project"

### Step 2: Enable Realtime Database
1. In Firebase Console, click "Realtime Database"
2. Click "Create Database"
3. Choose location closest to you
4. Start in **Test Mode** (we'll secure it later)
5. Copy the database URL (e.g., `https://pathfinder-4e3ff-default-rtdb.firebaseio.com/`)

### Step 3: Generate Service Account Key
1. Go to Project Settings (gear icon) → Service Accounts
2. Click "Generate New Private Key"
3. Click "Generate Key" to download JSON file
4. Save as `pathfinder-4e3ff-firebase-adminsdk-*.json` in project root
   ```bash
   # Move downloaded file to project root
   mv ~/Downloads/pathfinder-*-firebase-adminsdk-*.json /path/to/PathFinder/
   ```

### Step 4: Configure Environment Variables
```bash
cd ..  # Go back to project root
cp .env.example .env
nano .env  # or use any text editor
```

Update `.env` with your Firebase details:
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

Save and close (Ctrl+X, Y, Enter in nano).

---

## 5️⃣ Mobile App Setup

### Step 1: Navigate to Mobile App
```bash
cd mobile-app
```

### Step 2: Install Node Dependencies
```bash
npm install

# This will install:
# - expo (SDK 54)
# - react-native (0.81.5)
# - expo-camera (camera API)
# - expo-location (GPS)
# - expo-speech (text-to-speech)
# - expo-av (audio)
# - react-navigation (routing)
# - and more...
```

**Note**: This may take 3-5 minutes.

### Step 3: Configure Backend URL

Find your computer's IP address:

**Linux/macOS:**
```bash
ip addr show | grep "inet " | grep -v 127.0.0.1
# or
ifconfig | grep "inet "
```

**Windows:**
```cmd
ipconfig
```

Look for your local IP (e.g., `192.168.1.100` or `10.x.x.x`)

Now update the mobile app:
```bash
nano src/screens/CameraNavigationScreen.js
```

Find line 16 and update:
```javascript
const API_URL = 'http://YOUR_IP_HERE:8000/api';
// Example: const API_URL = 'http://192.168.1.100:8000/api';
```

Save and close.

---

## 6️⃣ Admin Dashboard Setup (Optional)

### Step 1: Navigate to Admin Dashboard
```bash
cd ../admin-dashboard
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Configure Environment
```bash
cp .env.example .env
nano .env
```

Add your Firebase config:
```env
REACT_APP_FIREBASE_API_KEY=your_api_key
REACT_APP_FIREBASE_AUTH_DOMAIN=pathfinder-4e3ff.firebaseapp.com
REACT_APP_FIREBASE_DATABASE_URL=https://pathfinder-4e3ff-default-rtdb.firebaseio.com/
REACT_APP_FIREBASE_PROJECT_ID=pathfinder-4e3ff
REACT_APP_API_URL=http://localhost:8000/api
```

---

## 7️⃣ Running the Application

### Terminal 1: Start Backend
```bash
cd backend
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

python3 run.py
```

**Expected output:**
```
INFO:     Starting PathFinder API
INFO:     Firebase initialized successfully
INFO:     API server started on 0.0.0.0:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Backend is now running!

### Terminal 2: Start Mobile App
Open a **new terminal**:
```bash
cd mobile-app
npx expo start --lan
```

**Expected output:**
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

### Terminal 3: Start Admin Dashboard (Optional)
Open a **new terminal**:
```bash
cd admin-dashboard
npm start
```

Dashboard opens at http://localhost:3000

---

## 8️⃣ Testing on Mobile Device

### Step 1: Connect to Same WiFi
**Important**: Your phone and computer MUST be on the same WiFi network!

### Step 2: Open Expo Go
- Open Expo Go app on your phone
- Tap "Scan QR Code"
- Scan the QR code from Terminal 2

### Step 3: Wait for App to Load
- First load may take 1-2 minutes
- You'll see "Building JavaScript bundle"
- Wait patiently...

### Step 4: Grant Permissions
When prompted, allow:
- ✅ Camera access
- ✅ Location access
- ✅ Microphone access

### Step 5: Test Object Detection
1. Point camera at objects (chair, table, door, person, cup, phone)
2. App automatically scans every 3 seconds
3. Listen for voice announcements:

**Example:**
> "I detect 2 objects: Chair at 2.5 meters on your left, Table at 3.1 meters in center"

### Step 6: Test Voice Commands (Demo Mode)
1. Tap the microphone button
2. Say: "What's around me?"
3. Listen for response

---

## 9️⃣ Verification Checklist

### Backend ✅
- [ ] Virtual environment activated
- [ ] All packages installed without errors
- [ ] YOLO model downloaded
- [ ] Firebase credentials configured
- [ ] Server running on port 8000
- [ ] Can access http://localhost:8000/docs

### Mobile App ✅
- [ ] Node packages installed
- [ ] API_URL updated with correct IP
- [ ] Expo server running
- [ ] QR code visible
- [ ] Phone on same WiFi as computer

### Mobile Device ✅
- [ ] Expo Go installed (SDK 54+)
- [ ] QR code scanned successfully
- [ ] App loaded without errors
- [ ] Camera permission granted
- [ ] Location permission granted
- [ ] Microphone permission granted
- [ ] Voice announcements working
- [ ] Objects being detected

---

## 🐛 Troubleshooting

### Problem: `ModuleNotFoundError: No module named 'fastapi'`
**Solution:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Problem: `Network request failed` on mobile
**Solutions:**
1. Ensure phone and computer on same WiFi
2. Check firewall isn't blocking port 8000
3. Try tunnel mode: `npx expo start --tunnel`
4. Update API_URL with correct IP address

### Problem: `YOLO model not found`
**Solution:**
```bash
cd backend
source venv/bin/activate
python3 -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

### Problem: Expo app crashes on startup
**Solutions:**
1. Clear Expo cache: `npx expo start -c`
2. Delete node_modules: `rm -rf node_modules && npm install`
3. Update Expo Go app on phone

### Problem: No voice announcements
**Solutions:**
1. Check phone volume
2. Check permissions in phone settings
3. Restart Expo app

### Problem: Slow detection (>5 seconds)
**Solutions:**
1. Reduce image quality in CameraNavigationScreen.js: `quality: 0.5` → `quality: 0.3`
2. Increase scan interval: `3000` → `5000`
3. Use faster model: YOLOv8n-tiny

---

## 📊 System Requirements Summary

### Minimum Requirements
- **OS**: Linux/macOS/Windows
- **RAM**: 4GB (8GB recommended)
- **Storage**: 5GB free
- **CPU**: Dual-core 2GHz+
- **Network**: WiFi

### Recommended Requirements
- **RAM**: 8GB+
- **Storage**: 10GB free
- **CPU**: Quad-core 2.5GHz+
- **GPU**: NVIDIA GPU (optional, for faster YOLO)

---

## 📚 Quick Reference

### Start Development
```bash
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python3 run.py

# Terminal 2 - Mobile
cd mobile-app && npx expo start --lan

# Terminal 3 - Admin (optional)
cd admin-dashboard && npm start
```

### Stop Everything
```bash
# Press Ctrl+C in each terminal
# Or kill processes:
pkill -f "python3 run.py"
pkill -f "expo start"
```

### Update Dependencies
```bash
# Backend
cd backend && source venv/bin/activate && pip install --upgrade -r requirements.txt

# Mobile
cd mobile-app && npm update

# Admin
cd admin-dashboard && npm update
```

---

## 🎓 Additional Resources

- **Full Installation Guide**: [INSTALLATION.md](INSTALLATION.md)
- **Testing Guide**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **API Documentation**: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **YOLO Guide**: [mobile-app/YOLO_INTEGRATION_GUIDE.md](mobile-app/YOLO_INTEGRATION_GUIDE.md)

---

## ✅ Success!

If you see:
- ✅ Backend: "API server started on 0.0.0.0:8000"
- ✅ Mobile: Expo QR code displayed
- ✅ Phone: App loaded and camera working
- ✅ Voice: "I detect X objects..."

**Congratulations! PathFinder AI is running! 🎉**

---

**Need Help?** Check [INSTALLATION.md](INSTALLATION.md) for detailed troubleshooting.

Last Updated: February 23, 2026
