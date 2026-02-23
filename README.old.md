# PathFinder 🧭

**AI-Powered Navigation Platform for Visually Impaired Users**

PathFinder provides real-time obstacle detection, voice assistance, and comprehensive analytics to help visually impaired individuals navigate safely.

---

## ✨ Features

### 👤 For Users (Visually Impaired)
- ✅ Voice-guided signup and login
- ✅ Real-time AI obstacle detection (YOLO v8)
- ✅ Direction-based alerts (left/right/center)  
- ✅ Distance estimation for hazards
- ✅ Voice-based complaint submission
- ✅ Session tracking and history

### 👨‍💼 For Admins
- ✅ Comprehensive analytics dashboard (React + Recharts)
- ✅ User activity and session monitoring
- ✅ Hazard detection analytics
- ✅ Complaint management system
- ✅ System efficiency metrics

---

## 🏗️ Architecture

```
PathFinder/
├── backend/               # FastAPI + AI Modules
│   ├── app/
│   │   ├── ai_modules/   # YOLO + Voice Assistant
│   │   ├── api/          # REST API Routes
│   │   ├── core/         # Security & Config
│   │   ├── models/       # Pydantic Schemas
│   │   └── services/     # Firebase Database
│   └── run.py
├── admin-dashboard/       # React.js Dashboard
│   └── src/
│       ├── components/   # Charts & UI
│       ├── pages/        # Dashboard & Complaints
│       └── services/     # API Client
├── user-mobile-app/       # React Native (Expo)
└── requirements.txt
```

---

## 🚀 Quick Start

### 1️⃣ Backend Setup

```bash
# Clone and navigate
git clone https://github.com/thanush2205/PathFinder.git
cd PathFinder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Firebase credentials

# Run backend
cd backend
python run.py
```
**Backend runs at:** http://localhost:8000  
**API Docs:** http://localhost:8000/docs

### 2️⃣ Admin Dashboard Setup

```bash
cd admin-dashboard
npm install
npm start
```
**Dashboard runs at:** http://localhost:3000

### 3️⃣ Create Admin User

```bash
curl -X POST http://localhost:8000/api/auth/signup \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "Admin",
    "email": "admin@pathfinder.com",
    "password": "Admin123!",
    "role": "admin"
  }'
```

---

## 🔧 Tech Stack

**Backend:**
- FastAPI (API Framework)
- YOLO v8 (Object Detection)
- OpenCV (Computer Vision)
- SpeechRecognition + gTTS (Voice)
- Firebase (Database)
- JWT (Authentication)

**Frontend:**
- React.js (Admin Dashboard)
- Recharts (Analytics Charts)
- Axios (HTTP Client)
- React Router (Navigation)

**Mobile:**
- React Native (Expo)

---

## 📡 Key API Endpoints

### Authentication
- `POST /api/auth/signup` - Register user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user

### AI Detection
- `POST /api/ai/detection/image/alert` - Get navigation alert from image
- `POST /api/ai/detection/frame/alert` - Real-time frame analysis

### Voice Assistant
- `POST /api/ai/voice/speech-to-text` - STT
- `POST /api/ai/voice/text-to-speech` - TTS
- `POST /api/ai/voice/process-command` - Voice command processing

### Analytics (Admin)
- `GET /api/analytics/dashboard` - Complete dashboard data
- `GET /api/analytics/users/trend` - User trend
- `GET /api/analytics/hazards/distribution` - Hazard stats

### Complaints
- `POST /api/complaints/` - Create complaint
- `GET /api/complaints/` - Get all (Admin)
- `PATCH /api/complaints/{id}` - Update status (Admin)

**Full Documentation:** http://localhost:8000/docs

---

## 🎙️ AI Voice Assistant Flow

### Role Selection
```
AI: "Welcome to PathFinder. Are you a User or an Admin?"
User: [Voice] "User"
→ User flow initiated
```

### Voice Signup
```
AI: "What is your name?"
User: "John Doe"

AI: "What is your email?"
User: "john@example.com"

AI: "Auto-generate password or speak your own?"
User: "Auto-generate"
→ Account created
```

### Navigation Alerts
```
[Camera detects obstacle]
AI: "Car detected left, approximately 3.5 meters away"
AI: "Person ahead center, 2 meters away"
```

---

## 📊 Dashboard Analytics

**Metrics Tracked:**
- Total Users & Active Users (daily/weekly)
- Navigation Sessions (count, duration, hazards)
- Hazard Detection Types (distribution)
- Complaint Status (open/resolved)
- System Efficiency (FPS, response time, uptime)

**Visualizations:**
- Line Chart: User registration trend
- Bar Chart: Session activity
- Pie Chart: Hazard distribution
- KPI Cards: Real-time metrics

---

## ⚙️ Configuration

**Environment Variables (`.env`):**

```env
# Backend
APP_NAME=PathFinder
PORT=8000
SECRET_KEY=your-secret-key-here

# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase-credentials.json
FIREBASE_DATABASE_URL=https://your-project.firebaseio.com

# AI
YOLO_MODEL_PATH=./models/yolov8n.pt
DETECTION_CONFIDENCE=0.5
DETECTION_FPS=20

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:19006
```

---

## 🗄️ Database Schema (Firebase)

### Users Collection
```json
{
  "user_id": {
    "name": "string",
    "email": "string",
    "role": "user|admin",
    "hashed_password": "string",
    "created_at": "ISO timestamp"
  }
}
```

### Sessions Collection
```json
{
  "session_id": {
    "user_id": "string",
    "start_time": "ISO timestamp",
    "end_time": "ISO timestamp",
    "hazards_detected": ["car", "person", ...],
    "duration_seconds": 123
  }
}
```

### Complaints Collection
```json
{
  "complaint_id": {
    "user_id": "string",
    "message": "string",
    "timestamp": "ISO timestamp",
    "status": "open|in_progress|resolved|closed",
    "admin_response": "string"
  }
}
```

---

## 📱 Mobile App (Coming Soon)

React Native app with:
- Voice-based authentication
- Real-time camera feed with detection
- Audio navigation alerts
- Voice complaint submission
- Session history

---

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend  
cd admin-dashboard
npm test
```

---

## 🐳 Docker Deployment

```bash
# Build backend
docker build -t pathfinder-backend ./backend

# Run backend
docker run -p 8000:8000 pathfinder-backend

# Build dashboard
docker build -t pathfinder-dashboard ./admin-dashboard
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open Pull Request

---

## 📄 License

MIT License - See LICENSE file

---

## 👥 Team & Support

**GitHub:** [thanush2205/PathFinder](https://github.com/thanush2205/PathFinder)  
**Issues:** GitHub Issues  
**Documentation:** API docs at `/docs`

---

## 🙏 Acknowledgments

- **YOLOv8** by Ultralytics
- **FastAPI** by Sebastián Ramírez
- **React** by Facebook
- **Recharts** for visualization

---

**Built with ❤️ for accessibility and inclusion**
