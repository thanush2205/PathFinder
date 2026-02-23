# PathFinder - Getting Started Guide

## 📋 Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.7 or higher installed
- [ ] Node.js 14 or higher installed
- [ ] Git installed
- [ ] Firebase account created
- [ ] Text editor or IDE (VS Code recommended)

---

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/thanush2205/PathFinder.git
cd PathFinder
```

### Step 2: Firebase Setup

1. **Create Firebase Project:**
   - Go to https://console.firebase.google.com/
   - Click "Add Project"
   - Enter project name: "PathFinder"
   - Follow the setup wizard

2. **Enable Realtime Database:**
   - In Firebase Console, go to "Realtime Database"
   - Click "Create Database"
   - Start in "Test Mode" (change to locked mode in production)
   - Copy your database URL (e.g., `https://pathfinder-xxxxx.firebaseio.com`)

3. **Generate Service Account Credentials:**
   - Go to Project Settings (⚙️ icon)
   - Click on "Service Accounts" tab
   - Click "Generate New Private Key"
   - Save the JSON file as `firebase-credentials.json`
   - Move it to the `PathFinder/backend/` directory

### Step 3: Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\\Scripts\\activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Backend Configuration
APP_NAME=PathFinder
ENVIRONMENT=development
DEBUG=True
API_VERSION=v1
HOST=0.0.0.0
PORT=8000

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=your-super-secret-key-change-this-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Firebase Configuration
FIREBASE_CREDENTIALS_PATH=./backend/firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project-id.firebaseio.com
FIREBASE_STORAGE_BUCKET=your-project-id.appspot.com

# CORS (Add your frontend URLs)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19006

# AI Configuration
YOLO_MODEL_PATH=./models/yolov8n.pt
DETECTION_CONFIDENCE=0.5
DETECTION_FPS=20

# Voice Assistant
TTS_ENGINE=gtts
STT_LANGUAGE=en-US
VOICE_TIMEOUT=5

# Logging
LOG_LEVEL=INFO
```

### Step 5: Download YOLO Model (Optional)

The YOLO model will be auto-downloaded on first run, or you can download manually:

```bash
# Create models directory
mkdir -p backend/models

# Download YOLOv8n model (lightweight, ~6MB)
# The ultralytics package will download automatically on first use
# Or manually download from: https://github.com/ultralytics/assets/releases
```

### Step 6: Start the Backend

```bash
cd backend
python run.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Verify Backend:**
- Open browser: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### Step 7: Admin Dashboard Setup

Open a new terminal window:

```bash
cd admin-dashboard

# Install Node.js dependencies
npm install

# Start development server
npm start
```

The dashboard should automatically open at http://localhost:3000

### Step 8: Create Admin User

Use the API to create your first admin account:

**Option 1: Using cURL**
```bash
curl -X POST http://localhost:8000/api/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Admin User",
    "email": "admin@pathfinder.com",
    "password": "SecureAdmin123!",
    "role": "admin"
  }'
```

**Option 2: Using Swagger UI**
1. Go to http://localhost:8000/docs
2. Find `/api/auth/signup` endpoint
3. Click "Try it out"
4. Fill in the request body:
   ```json
   {
     "name": "Admin User",
     "email": "admin@pathfinder.com",
     "password": "SecureAdmin123!",
     "role": "admin"
   }
   ```
5. Click "Execute"

**Option 3: Using Python script**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/auth/signup",
    json={
        "name": "Admin User",
        "email": "admin@pathfinder.com",
        "password": "SecureAdmin123!",
        "role": "admin"
    }
)

print(response.json())
```

### Step 9: Login to Dashboard

1. Open http://localhost:3000
2. Enter credentials:
   - Email: `admin@pathfinder.com`
   - Password: `SecureAdmin123!`
3. Click "Login"

You should now see the admin dashboard!

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend running on http://localhost:8000
- [ ] API docs accessible at http://localhost:8000/docs
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] Admin dashboard running on http://localhost:3000
- [ ] Can login to admin dashboard
- [ ] Dashboard displays analytics (even if empty)
- [ ] Firebase connection successful (check backend logs)

---

## 🧪 Testing the System

### Test 1: Create a Regular User

```bash
curl -X POST http://localhost:8000/api/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Test User",
    "email": "user@test.com",
    "password": "TestUser123!",
    "role": "user"
  }'
```

### Test 2: Start a Navigation Session

First, login and get the token:
```bash
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \\
  -H "Content-Type: application/json" \\
  -d '{"email":"user@test.com","password":"TestUser123!"}' \\
  | jq -r '.access_token')

# Create session
curl -X POST http://localhost:8000/api/sessions/ \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{"user_id":"user_id_from_signup"}'
```

### Test 3: Submit a Complaint

```bash
curl -X POST http://localhost:8000/api/complaints/ \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_id": "user_id_from_signup",
    "message": "This is a test complaint"
  }'
```

### Test 4: Check Analytics Dashboard

1. Login to admin dashboard
2. Navigate to Dashboard page
3. You should see the test user and complaint

### Test 5: AI Detection (Image Upload)

Using the Swagger UI at http://localhost:8000/docs:
1. Find `/api/ai/detection/image/alert`
2. Click "Try it out"
3. Upload a test image
4. Click "Execute"
5. Check the navigation alert response

---

## 🔧 Troubleshooting

### Problem: Backend won't start

**Solution 1: Check Python version**
```bash
python --version  # Should be 3.7+
```

**Solution 2: Reinstall dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

**Solution 3: Check port availability**
```bash
# On Linux/Mac
lsof -i :8000

# On Windows
netstat -ano | findstr :8000
```

### Problem: Firebase connection error

**Solution:**
1. Verify `firebase-credentials.json` is in `backend/` folder
2. Check Firebase Database URL in `.env`
3. Ensure Firebase Realtime Database is created and in test mode
4. Check Firebase project permissions

### Problem: Admin dashboard won't load

**Solution:**
```bash
cd admin-dashboard

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Start again
npm start
```

### Problem: YOLO model not loading

**Solution:**
The model downloads automatically. If it fails:
1. Check internet connection
2. Download manually from: https://github.com/ultralytics/assets/releases
3. Place `yolov8n.pt` in `backend/models/` directory
4. Update `YOLO_MODEL_PATH` in `.env`

### Problem: CORS errors in dashboard

**Solution:**
Update `.env`:
```env
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

Restart backend after changes.

---

## 📱 Next Steps

1. **Mobile App Development:**
   - Set up React Native Expo project in `user-mobile-app/`
   - Implement camera integration
   - Add voice assistant UI

2. **Enhancements:**
   - Add more hazard detection classes
   - Improve voice recognition accuracy
   - Add multi-language support
   - Implement offline mode

3. **Production Deployment:**
   - Deploy backend to Heroku/AWS/GCP
   - Deploy dashboard to Vercel/Netlify
   - Configure production Firebase
   - Set up SSL certificates
   - Enable proper security settings

---

## 📚 Additional Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **React Documentation:** https://react.dev/
- **YOLOv8 Documentation:** https://docs.ultralytics.com/
- **Firebase Documentation:** https://firebase.google.com/docs
- **Project Repository:** https://github.com/thanush2205/PathFinder

---

## 🆘 Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Review backend logs for error messages
3. Check browser console for frontend errors
4. Open an issue on GitHub
5. Review API documentation at `/docs`

---

## 🎉 Success!

If you've completed all steps and tests pass, congratulations! You now have a fully functional PathFinder system running locally.

**What's working:**
✅ Backend API with AI modules  
✅ Admin dashboard with analytics  
✅ User authentication (JWT)  
✅ Database (Firebase)  
✅ Object detection (YOLO)  
✅ Voice assistant (STT/TTS)  
✅ Complaint management  
✅ Session tracking  

**Next:** Start developing the mobile app or customize the existing features to your needs!

---

**Need more help? Check the full documentation in README.md and API_DOCUMENTATION.md**
