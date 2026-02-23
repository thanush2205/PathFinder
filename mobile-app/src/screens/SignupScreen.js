import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  Alert,
  ActivityIndicator,
} from 'react-native';
import * as Speech from 'expo-speech';

const API_URL = 'http://10.15.45.243:8000/api';

export default function SignupScreen({ navigation }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);

  useEffect(() => {
    // Welcome message when screen loads
    speak('Welcome to PathFinder. Let me help you create an account. Please enter your name.');
  }, []);

  const speak = (text) => {
    Speech.speak(text, {
      language: 'en-US',
      pitch: 1.0,
      rate: 0.9,
    });
  };

  const handleSignup = async () => {
    if (!name || !email || !password) {
      speak('Please fill in all fields');
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    setLoading(true);
    speak('Creating your account. Please wait.');

    try {
      const response = await fetch(`${API_URL}/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          email,
          password,
          role: 'user',
        }),
      });

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.detail || 'Signup failed');
      }

      speak('Account created successfully! Taking you to camera navigation.');
      
      setTimeout(() => {
        navigation.replace('Camera', { 
          token: data.access_token,
          user: data.user 
        });
      }, 2000);

    } catch (error) {
      const message = error.message || 'Signup failed. Please try again.';
      speak(message);
      Alert.alert('Signup Failed', message);
    } finally {
      setLoading(false);
    }
  };

  const handleFieldFocus = (field) => {
    const messages = {
      name: 'Enter your full name',
      email: 'Enter your email address',
      password: 'Enter a password with at least 8 characters',
    };
    speak(messages[field]);
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>PathFinder</Text>
        <Text style={styles.subtitle}>AI Navigation Assistant</Text>
      </View>

      <View style={styles.form}>
        <View style={styles.inputContainer}>
          <Text style={styles.label}>Name</Text>
          <TextInput
            style={styles.input}
            placeholder="Your full name"
            placeholderTextColor="#999"
            value={name}
            onChangeText={setName}
            onFocus={() => handleFieldFocus('name')}
            accessibilityLabel="Name input field"
            accessibilityHint="Enter your full name"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Email</Text>
          <TextInput
            style={styles.input}
            placeholder="your.email@example.com"
            placeholderTextColor="#999"
            value={email}
            onChangeText={setEmail}
            onFocus={() => handleFieldFocus('email')}
            keyboardType="email-address"
            autoCapitalize="none"
            accessibilityLabel="Email input field"
            accessibilityHint="Enter your email address"
          />
        </View>

        <View style={styles.inputContainer}>
          <Text style={styles.label}>Password</Text>
          <TextInput
            style={styles.input}
            placeholder="Minimum 8 characters"
            placeholderTextColor="#999"
            value={password}
            onChangeText={setPassword}
            onFocus={() => handleFieldFocus('password')}
            secureTextEntry
            accessibilityLabel="Password input field"
            accessibilityHint="Enter a password with at least 8 characters"
          />
        </View>

        <TouchableOpacity
          style={[styles.button, loading && styles.buttonDisabled]}
          onPress={handleSignup}
          disabled={loading}
          accessibilityLabel="Sign up button"
          accessibilityHint="Double tap to create your account"
        >
          {loading ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Sign Up</Text>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          style={styles.linkButton}
          onPress={() => {
            speak('Going to login screen');
            navigation.navigate('Login');
          }}
          accessibilityLabel="Already have account link"
          accessibilityHint="Double tap to go to login screen"
        >
          <Text style={styles.linkText}>
            Already have an account? Login
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
    padding: 20,
  },
  header: {
    marginTop: 60,
    marginBottom: 40,
    alignItems: 'center',
  },
  title: {
    fontSize: 42,
    fontWeight: 'bold',
    color: '#fff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 18,
    color: '#0f3460',
  },
  form: {
    flex: 1,
  },
  inputContainer: {
    marginBottom: 20,
  },
  label: {
    fontSize: 16,
    color: '#fff',
    marginBottom: 8,
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#16213e',
    borderRadius: 12,
    padding: 16,
    fontSize: 16,
    color: '#fff',
    borderWidth: 2,
    borderColor: '#0f3460',
  },
  button: {
    backgroundColor: '#e94560',
    borderRadius: 12,
    padding: 18,
    alignItems: 'center',
    marginTop: 10,
    elevation: 3,
    shadowColor: '#e94560',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 4,
  },
  buttonDisabled: {
    backgroundColor: '#994560',
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  linkButton: {
    marginTop: 20,
    alignItems: 'center',
  },
  linkText: {
    color: '#e94560',
    fontSize: 16,
  },
});
