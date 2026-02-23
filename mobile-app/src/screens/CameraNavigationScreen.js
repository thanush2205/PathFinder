import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ScrollView,
  Platform,
} from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';
import * as Speech from 'expo-speech';
import * as Location from 'expo-location';
import { Audio } from 'expo-av';

const API_URL = 'http://10.15.45.243:8000/api';

export default function CameraNavigationScreen({ route, navigation }) {
  // Optional token and user from route params (if authentication is enabled)
  const token = route?.params?.token || null;
  const user = route?.params?.user || { name: 'User' };
  
  const [permission, requestPermission] = useCameraPermissions();
  const [isListening, setIsListening] = useState(false);
  const [detectedObjects, setDetectedObjects] = useState([]);
  const [aiResponse, setAiResponse] = useState('');
  const [isScanning, setIsScanning] = useState(false);
  const [location, setLocation] = useState(null);
  const [recording, setRecording] = useState(null);
  const [isProcessingVoice, setIsProcessingVoice] = useState(false);
  
  const cameraRef = useRef(null);
  const scanInterval = useRef(null);

  useEffect(() => {
    initializeServices();
    
    return () => {
      if (scanInterval.current) {
        clearInterval(scanInterval.current);
      }
      if (recording) {
        recording.stopAndUnloadAsync();
      }
    };
  }, [permission]);

  const initializeServices = async () => {
    // Request location permission
    const { status: locationStatus } = await Location.requestForegroundPermissionsAsync();
    if (locationStatus !== 'granted') {
      speak('Location permission denied. I cannot provide navigation assistance.');
      return;
    }

    // Request audio permission for voice input
    const { status: audioStatus } = await Audio.requestPermissionsAsync();
    if (audioStatus !== 'granted') {
      speak('Microphone permission denied. I cannot listen to your voice commands.');
      return;
    }

    // Get current location
    try {
      const currentLocation = await Location.getCurrentPositionAsync({});
      setLocation(currentLocation);
    } catch (error) {
      console.log('Location error:', error);
    }

    if (permission?.granted) {
      speak(`Welcome ${user.name}! I am your AI navigation assistant. The camera and location services are ready. I'm listening for your voice commands. Just speak naturally, and I will help you navigate.`);
      
      // Start continuous object detection
      startContinuousScanning();
      
      // Start voice listening
      startContinuousVoiceListening();
    }
  };

  const speak = (text) => {
    Speech.speak(text, {
      language: 'en-US',
      pitch: 1.0,
      rate: 0.85,
    });
    setAiResponse(text);
  };

  const startScanning = async () => {
    setIsScanning(true);
    speak('Starting environment scan. I will detect objects and obstacles around you.');
    
    // Simulate continuous scanning
    scanInterval.current = setInterval(async () => {
      await detectObjects();
    }, 3000); // Scan every 3 seconds
  };

  const stopScanning = () => {
    setIsScanning(false);
    if (scanInterval.current) {
      clearInterval(scanInterval.current);
      scanInterval.current = null;
    }
    speak('Scanning stopped.');
  };

  const detectObjects = async () => {
    if (!cameraRef.current || !hasPermission) {
      return;
    }

    try {
      // Take photo from camera
      const photo = await cameraRef.current.takePictureAsync({
        quality: 0.5,
        base64: true,
      });

      // Get current location
      let currentLocation = null;
      if (location) {
        currentLocation = {
          latitude: location.coords.latitude,
          longitude: location.coords.longitude,
        };
      }

      // Call YOLO backend API
      const response = await fetch(`${API_URL}/detection/yolo`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: photo.base64,
          location: currentLocation,
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();
      
      // Update detected objects
      setDetectedObjects(data.objects || []);
      
      // Speak the natural language message
      if (data.message) {
        speak(data.message);
      } else if (data.total_detected > 0) {
        const alert = `Detected ${data.total_detected} objects: ${data.objects.map(o => `${o.label} at ${o.distance}`).join(', ')}`;
        speak(alert);
      } else {
        speak('No objects detected in view.');
      }
    } catch (error) {
      console.error('Detection error:', error);
      // Fallback to demo mode on error
      useDemoDetection();
    }
  };

  const useDemoDetection = () => {
    const demoObjects = [
      { label: 'Chair', distance: '2.5m', position: 'center', confidence: 0.85 },
      { label: 'Table', distance: '3.2m', position: 'right', confidence: 0.92 },
    ];
    setDetectedObjects(demoObjects);
    speak(`Demo mode: Detected ${demoObjects.length} objects`);
  };

  const handleVoiceCommand = async (command) => {
    setIsListening(true);
    speak(`Processing your command: ${command}`);

    try {
      // Demo responses (no backend required)
      let response = '';
      if (command.includes('Where')) {
        response = 'You are in a room. There is a door 5 meters to your left, and furniture ahead.';
      } else if (command.includes('Around')) {
        response = 'I detect 3 objects around you: a chair 2 meters ahead, a table 3 meters to the right, and a door 5 meters to the left.';
      } else if (command.includes('Navigate')) {
        response = 'To reach the door, turn left and walk forward 5 meters. I will guide you step by step.';
      } else if (command.includes('Read')) {
        response = 'Reading text from the environment. Please point the camera at the text you want me to read.';
      } else {
        response = 'Command received. How can I assist you?';
      }
      
      speak(response);
    } catch (error) {
      speak('Sorry, I could not process that command. Please try again.');
    } finally {
      setIsListening(false);
    }
  };

  if (!permission) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>Loading camera...</Text>
      </View>
    );
  }

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.message}>Camera permission required</Text>
        <TouchableOpacity style={styles.permissionButton} onPress={requestPermission}>
          <Text style={styles.permissionButtonText}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* Camera View */}
      <View style={styles.cameraContainer}>
        <CameraView
          ref={cameraRef}
          style={styles.camera}
          facing="back"
        />
        {/* Overlay with detection info - positioned absolutely */}
        <View style={styles.overlay}>
          <Text style={styles.statusText}>
            {isScanning ? '🔴 Scanning...' : '⚪ Ready'}
          </Text>
          
          {detectedObjects.length > 0 && (
            <View style={styles.detectionBox}>
              {detectedObjects.map((obj, index) => (
                <Text key={index} style={styles.detectionText}>
                  {obj.label} - {obj.distance} ({obj.position})
                </Text>
              ))}
            </View>
          )}
        </View>
      </View>

      {/* AI Response Display */}
      <View style={styles.responseContainer}>
        <Text style={styles.responseLabel}>AI Assistant:</Text>
        <ScrollView style={styles.responseScroll}>
          <Text style={styles.responseText}>
            {aiResponse || 'Waiting for command...'}
          </Text>
        </ScrollView>
      </View>

      {/* Control Buttons */}
      <View style={styles.controlsContainer}>
        <TouchableOpacity
          style={[styles.scanButton, isScanning && styles.scanningButton]}
          onPress={isScanning ? stopScanning : startScanning}
          accessibilityLabel={isScanning ? 'Stop scanning' : 'Start scanning'}
        >
          <Text style={styles.scanButtonText}>
            {isScanning ? '⏸️ Stop Scan' : '▶️ Start Scan'}
          </Text>
        </TouchableOpacity>

        <View style={styles.commandButtons}>
          <TouchableOpacity
            style={styles.commandButton}
            onPress={() => handleVoiceCommand('where am i')}
            accessibilityLabel="Ask where am I"
          >
            <Text style={styles.commandButtonText}>📍 Where Am I?</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.commandButton}
            onPress={() => handleVoiceCommand("what's around me")}
            accessibilityLabel="Ask what's around me"
          >
            <Text style={styles.commandButtonText}>👁️ What's Around?</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.commandButton}
            onPress={() => handleVoiceCommand('help me navigate')}
            accessibilityLabel="Start navigation"
          >
            <Text style={styles.commandButtonText}>🧭 Navigate</Text>
          </TouchableOpacity>

          <TouchableOpacity
            style={styles.commandButton}
            onPress={() => handleVoiceCommand('read text')}
            accessibilityLabel="Read text"
          >
            <Text style={styles.commandButtonText}>📖 Read Text</Text>
          </TouchableOpacity>
        </View>

        <TouchableOpacity
          style={styles.logoutButton}
          onPress={() => {
            speak('Logging out');
            navigation.replace('Login');
          }}
          accessibilityLabel="Logout"
        >
          <Text style={styles.logoutButtonText}>Logout</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  cameraContainer: {
    flex: 2,
    overflow: 'hidden',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.3)',
    padding: 20,
  },
  statusText: {
    fontSize: 24,
    color: '#fff',
    fontWeight: 'bold',
    textAlign: 'center',
    marginTop: 40,
  },
  detectionBox: {
    marginTop: 20,
    backgroundColor: 'rgba(233, 69, 96, 0.9)',
    borderRadius: 12,
    padding: 15,
  },
  detectionText: {
    color: '#fff',
    fontSize: 16,
    marginVertical: 4,
    fontWeight: '600',
  },
  responseContainer: {
    backgroundColor: '#16213e',
    padding: 15,
    borderTopWidth: 2,
    borderTopColor: '#0f3460',
  },
  responseLabel: {
    color: '#fff',
    fontSize: 14,
    fontWeight: 'bold',
    marginBottom: 5,
  },
  responseScroll: {
    maxHeight: 80,
  },
  responseText: {
    color: '#fff',
    fontSize: 16,
    lineHeight: 22,
  },
  controlsContainer: {
    padding: 15,
    backgroundColor: '#1a1a2e',
  },
  scanButton: {
    backgroundColor: '#e94560',
    borderRadius: 12,
    padding: 18,
    alignItems: 'center',
    marginBottom: 15,
  },
  scanningButton: {
    backgroundColor: '#ff6b6b',
  },
  scanButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  commandButtons: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginBottom: 15,
  },
  commandButton: {
    backgroundColor: '#0f3460',
    borderRadius: 10,
    padding: 12,
    width: '48%',
    marginBottom: 10,
    alignItems: 'center',
  },
  commandButtonText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  logoutButton: {
    backgroundColor: '#16213e',
    borderRadius: 10,
    padding: 12,
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#e94560',
  },
  logoutButtonText: {
    color: '#e94560',
    fontSize: 16,
    fontWeight: '600',
  },
  message: {
    color: '#fff',
    fontSize: 18,
    textAlign: 'center',
    marginTop: 100,
  },
  subtitle: {
    color: '#999',
    fontSize: 14,
    textAlign: 'center',
    marginTop: 10,
  },
});
