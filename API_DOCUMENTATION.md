# PathFinder API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All protected endpoints require a JWT Bearer token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

---

## Endpoints

### 🔐 Authentication

#### Register User
```http
POST /auth/signup
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "role": "user",
  "auto_generate_password": false
}

Response 201:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "user",
    "created_at": "2026-02-14T00:00:00"
  }
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "admin@pathfinder.com",
  "password": "Admin123!"
}

Response 200:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer",
  "user": { ... }
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>

Response 200:
{
  "id": "user_id",
  "name": "John Doe",
  "email": "john@example.com",
  "role": "user",
  "created_at": "2026-02-14T00:00:00"
}
```

---

### 🤖 AI Detection

#### Detect Objects in Image
```http
POST /ai/detection/image
Authorization: Bearer <token>
Content-Type: multipart/form-data

image: <file>

Response 200:
[
  {
    "class_name": "car",
    "confidence": 0.95,
    "bbox": [100, 150, 400, 500],
    "distance": 3.5,
    "direction": "left"
  }
]
```

#### Get Navigation Alert
```http
POST /ai/detection/image/alert
Authorization: Bearer <token>
Content-Type: multipart/form-data

image: <file>

Response 200:
{
  "alert_type": "car",
  "message": "Car detected left, approximately 3.5 meters away",
  "severity": "high",
  "detections": [...]
}
```

#### Real-time Frame Detection
```http
POST /ai/detection/frame/alert
Authorization: Bearer <token>
Content-Type: application/json

{
  "frame": "base64_encoded_image_data"
}

Response 200:
{
  "alert_type": "person",
  "message": "Person detected center, approximately 2.0 meters away",
  "severity": "high",
  "detections": [...]
}
```

---

### 🎙️ Voice Assistant

#### Speech to Text
```http
POST /ai/voice/speech-to-text
Authorization: Bearer <token>
Content-Type: multipart/form-data

audio: <file>

Response 200:
{
  "text": "I want to start navigation"
}
```

#### Text to Speech
```http
POST /ai/voice/text-to-speech
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "Welcome to PathFinder"
}

Response 200:
{
  "audio": "base64_encoded_mp3_data",
  "format": "mp3",
  "encoding": "base64"
}
```

#### Process Voice Command
```http
POST /ai/voice/process-command
Authorization: Bearer <token>
Content-Type: application/json

{
  "text": "Start navigation",
  "audio_data": null
}

Response 200:
{
  "text": "Starting navigation. I'll alert you about obstacles ahead.",
  "audio_url": "base64_audio_data",
  "action": "start_navigation",
  "data": null
}
```

---

### 📊 Analytics (Admin Only)

#### Get Dashboard Analytics
```http
GET /analytics/dashboard
Authorization: Bearer <admin_token>

Response 200:
{
  "users": {
    "total_users": 150,
    "active_users_today": 45,
    "active_users_week": 89,
    "new_users_today": 5
  },
  "sessions": {
    "total_sessions": 1200,
    "sessions_today": 78,
    "average_duration_minutes": 15.5,
    "total_hazards_detected": 4500
  },
  "hazards": [
    {"hazard_type": "car", "count": 1200},
    {"hazard_type": "person", "count": 900}
  ],
  "complaints": {
    "total_complaints": 25,
    "open_complaints": 5,
    "resolved_complaints": 18,
    "average_resolution_time_hours": 24.5
  },
  "system_efficiency": {
    "average_response_time_ms": 150,
    "detection_fps": 18,
    "api_uptime_percent": 99.9
  }
}
```

#### Get User Trend
```http
GET /analytics/users/trend?days=7
Authorization: Bearer <admin_token>

Response 200:
{
  "trend": [
    {"date": "2026-02-08", "count": 5},
    {"date": "2026-02-09", "count": 8},
    ...
  ]
}
```

---

### 💬 Complaints

#### Create Complaint
```http
POST /complaints/
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": "user_id",
  "message": "The navigation alert was delayed"
}

Response 201:
{
  "id": "complaint_id",
  "user_id": "user_id",
  "message": "The navigation alert was delayed",
  "timestamp": "2026-02-14T10:30:00",
  "status": "open",
  "admin_response": null
}
```

#### Get All Complaints (Admin)
```http
GET /complaints/?status_filter=open
Authorization: Bearer <admin_token>

Response 200:
[
  {
    "id": "complaint_id",
    "user_id": "user_id",
    "message": "...",
    "timestamp": "2026-02-14T10:30:00",
    "status": "open",
    "admin_response": null
  }
]
```

#### Update Complaint (Admin)
```http
PATCH /complaints/{complaint_id}
Authorization: Bearer <admin_token>
Content-Type: application/json

{
  "status": "resolved",
  "admin_response": "Thank you for reporting. Issue has been fixed."
}

Response 200:
{
  "id": "complaint_id",
  ...
}
```

---

### 📱 Sessions

#### Start Session
```http
POST /sessions/
Authorization: Bearer <token>
Content-Type: application/json

{
  "user_id": "user_id"
}

Response 201:
{
  "id": "session_id",
  "user_id": "user_id",
  "start_time": "2026-02-14T10:00:00",
  "end_time": null,
  "hazards_detected": [],
  "duration_seconds": null
}
```

#### Update Session
```http
PATCH /sessions/{session_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "hazards_detected": ["car", "person"],
  "end_time": "2026-02-14T10:15:00"
}

Response 200:
{
  "id": "session_id",
  "user_id": "user_id",
  "start_time": "2026-02-14T10:00:00",
  "end_time": "2026-02-14T10:15:00",
  "hazards_detected": ["car", "person"],
  "duration_seconds": 900
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied. Required role: admin"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Rate Limiting

- Detection endpoints: 60 requests/minute
- Voice endpoints: 30 requests/minute
- Other endpoints: 100 requests/minute

---

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation with the ability to test endpoints directly.
