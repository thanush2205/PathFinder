# PathFinder AI - Testing Guide

## Current Status ✅

### Backend (YOLO Integrated)
- ✅ FastAPI server running on http://10.15.45.243:8000
- ✅ YOLO detection endpoint: `/api/detection/yolo`
- ✅ YOLOv8n model loaded successfully
- ✅ Firebase database connected
- Process ID: 203314

### Mobile App (Real AI Detection)
- ✅ Expo running in tunnel mode
- ✅ Camera permissions configured
- ✅ Location services integrated
- ✅ Text-to-speech working
- ✅ YOLO backend integration complete

## How to Test

### 1. Open Mobile App
```bash
cd /home/thanush/Desktop/pathFinder/PathFinder/mobile-app
# Expo is already running, just scan the QR code
```

Look for the QR code in the terminal where Expo is running (pts/26).

### 2. Scan QR Code
- Open **Expo Go** app on your phone (must be SDK 54)
- Scan the QR code from the terminal
- Wait for app to load

### 3. Grant Permissions
When the app starts, it will ask for:
1. Camera permission - **Allow**
2. Location permission - **Allow** 
3. Microphone permission - **Allow**

### 4. Test Object Detection

The app will:
1. Automatically start scanning every 3 seconds
2. Take a photo
3. Send to YOLO backend
4. Announce detected objects via voice

**Point your camera at:**
- Chairs
- Tables
- Doors
- People
- Cups
- Phones
- Laptops
- Any common objects

**You'll hear:**
> "I detect 3 objects: Chair at 2.5 meters on your left, Table at 3.1 meters ahead in center, Door at 4.8 meters on your right"

### 5. Test Voice Commands (Demo Mode)

Tap the **microphone button** and say:
- "Where am I?" - Get location context
- "What's around me?" - List nearby objects
- "Navigate to exit" - Get navigation guidance
- "Read text" - OCR mode (future feature)

**Note:** Voice input is currently in demo mode. Real speech-to-text requires:
- Google Cloud Speech-to-Text
- Azure Speech Services
- AWS Transcribe

## Current Features

### ✅ Working
1. **Real-time Object Detection** (YOLO)
   - YOLOv8n model
   - Detects 80+ object classes
   - Distance estimation (based on FOV calculations)
   - Position detection (left/center/right)
   - Confidence filtering (>50%)

2. **GPS Location Tracking**
   - Continuous location updates
   - Latitude/longitude sent to backend
   - Future: Indoor mapping

3. **Text-to-Speech Announcements**
   - Natural language descriptions
   - Automatic scanning announcements
   - Voice command feedback

4. **Continuous Scanning**
   - Scans every 3 seconds automatically
   - Can start/stop manually

### 🔄 In Progress
1. **Voice Input (Speech-to-Text)**
   - Currently: Demo responses only
   - Next: Integrate Google Cloud Speech API
   - User can speak commands without tapping buttons

2. **Distance Calibration**
   - Current: Estimated using FOV (60°) and object height (1.5m)
   - Next: Real-world testing and calibration

### ❌ Not Yet Implemented
1. Navigation pathfinding algorithm
2. OCR text reading
3. Obstacle avoidance guidance
4. Indoor mapping
5. Offline caching

## Troubleshooting

### Backend Not Responding
```bash
# Check if backend is running
ps aux | grep "python3 run.py"

# Restart backend if needed
cd /home/thanush/Desktop/pathFinder/PathFinder/backend
pkill -f "python3 run.py"
nohup python3 run.py > backend.log 2>&1 &

# Check logs
tail -f backend.log
```

### Mobile App Network Error
1. Make sure both phone and laptop are on same WiFi
2. Check IP address: `ip addr show | grep "inet 10"`
3. Use tunnel mode if LAN doesn't work (already configured)
4. Verify API_URL in CameraNavigationScreen.js: `http://10.15.45.243:8000/api`

### Camera Not Working
1. Check Expo SDK version: Must be 54.0.x
2. Verify expo-camera version: `~17.0.10`
3. Grant permissions in phone settings if denied
4. Restart app after granting permissions

### YOLO Detection Slow
- Current: CPU-only inference (~2-3 seconds per frame)
- Solution: Deploy backend on GPU server
- Alternative: Reduce image quality (currently 0.5, try 0.3)

## API Testing

Test backend directly:
```bash
# Health check
curl http://10.15.45.243:8000/

# API docs
curl http://10.15.45.243:8000/docs

# Test YOLO endpoint (requires valid base64 image)
curl -X POST http://10.15.45.243:8000/api/detection/yolo \
  -H "Content-Type: application/json" \
  -d '{"image":"<base64_string>","location":{"latitude":37.7749,"longitude":-122.4194}}'
```

## Next Steps

### Immediate (This Session)
1. ✅ YOLO backend integration - DONE
2. ✅ Mobile app YOLO connection - DONE
3. 🔄 Test end-to-end detection - IN TESTING
4. ⏳ Calibrate distance estimation
5. ⏳ Add error handling for network failures

### Short-term (Next Session)
1. Integrate speech-to-text service
2. Remove demo voice commands
3. Add object tracking between frames
4. Optimize detection speed
5. Add navigation pathfinding

### Long-term
1. Deploy backend on cloud with GPU
2. Implement indoor mapping
3. Add OCR for text reading
4. Create admin dashboard analytics
5. App store deployment (iOS/Android)

## Contact & Support

- Backend logs: `/home/thanush/Desktop/pathFinder/PathFinder/backend/backend.log`
- Mobile app logs: Check Expo terminal (pts/26)
- YOLO integration: See `YOLO_INTEGRATION_GUIDE.md`
