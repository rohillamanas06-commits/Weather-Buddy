from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import speech_recognition as sr
import pyttsx3
import requests
import json
import os
from datetime import datetime
import threading
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY environment variable is required")
recognizer = sr.Recognizer()

# Initialize TTS engine
try:
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[1].id if len(voices) > 1 else voices[0].id)
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.8)
except:
    engine = None

class VoiceAssistant:
    def __init__(self):
        self.is_listening = False
        self.last_response = ""
    
    def speak(self, text):
        """Convert text to speech"""
        if engine:
            try:
                engine.say(text)
                engine.runAndWait()
            except:
                pass
        return text
    
    def get_weather(self, city):
        """Get weather information for a city"""
        try:
            base_url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            }
            response = requests.get(base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                weather_info = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'humidity': data['main']['humidity'],
                    'pressure': data['main']['pressure'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon'],
                    'wind_speed': data['wind']['speed'],
                    'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                    'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                    'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
                }
                
                weather_text = f"The weather in {weather_info['city']} is {weather_info['temperature']}°C with {weather_info['description']}. It feels like {weather_info['feels_like']}°C with {weather_info['humidity']}% humidity."
                
                return {
                    'success': True,
                    'data': weather_info,
                    'message': weather_text
                }
            else:
                return {
                    'success': False,
                    'message': f"Could not find weather data for {city}. Please check the city name."
                }
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'message': "Weather service is taking too long to respond. Please try again."
            }
        except Exception as e:
            return {
                'success': False,
                'message': "Sorry, I couldn't fetch the weather information right now."
            }
    
    def process_voice_command(self, text):
        """Process voice commands"""
        text = text.lower().strip()
        
        if "weather" in text:
            # Extract city name
            words = text.split()
            city = None
            
            if "in" in words:
                city_index = words.index("in") + 1
                if city_index < len(words):
                    city = " ".join(words[city_index:])
            elif "for" in words:
                city_index = words.index("for") + 1
                if city_index < len(words):
                    city = " ".join(words[city_index:])
            else:
                # Try to extract city from common patterns
                weather_keywords = ["weather", "temperature", "temp", "climate"]
                for keyword in weather_keywords:
                    if keyword in text:
                        remaining = text.replace(keyword, "").strip()
                        if remaining:
                            city = remaining
                        break
            
            if city:
                return self.get_weather(city)
            else:
                return {
                    'success': False,
                    'message': "Please specify a city. For example, say 'weather in London' or 'weather for New York'."
                }
        
        elif "hello" in text or "hi" in text or "hey" in text:
            return {
                'success': True,
                'message': "Hello! I'm your voice assistant. I can help you with weather information. Just ask me about the weather in any city!"
            }
        
        elif "help" in text:
            return {
                'success': True,
                'message': "I can help you with weather information. Try saying 'weather in [city name]' or 'what's the weather like in [city name]'."
            }
        
        elif "time" in text:
            current_time = datetime.now().strftime("%H:%M")
            return {
                'success': True,
                'message': f"The current time is {current_time}."
            }
        
        elif "date" in text:
            current_date = datetime.now().strftime("%B %d, %Y")
            return {
                'success': True,
                'message': f"Today is {current_date}."
            }
        
        else:
            return {
                'success': False,
                'message': "I can help you with weather information, time, and date. Try asking about the weather in a city!"
            }

# Initialize assistant
assistant = VoiceAssistant()

# Routes
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/weather', methods=['POST'])
def get_weather():
    """Get weather for a specific city"""
    try:
        data = request.get_json()
        city = data.get('city', '').strip()
        
        if not city:
            return jsonify({
                'success': False,
                'message': 'Please provide a city name.'
            }), 400
        
        result = assistant.get_weather(city)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your request.'
        }), 500

@app.route('/api/voice/recognize', methods=['POST'])
def recognize_voice():
    """Process voice recognition"""
    try:
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No audio file provided.'
            }), 400
        
        audio_file = request.files['audio']
        
        # Save temporary audio file
        temp_path = 'temp_audio.wav'
        audio_file.save(temp_path)
        
        try:
            # Recognize speech
            with sr.AudioFile(temp_path) as source:
                audio = recognizer.record(source)
            
            text = recognizer.recognize_google(audio)
            
            # Process the command
            result = assistant.process_voice_command(text)
            result['recognized_text'] = text
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            return jsonify(result)
        
        except sr.UnknownValueError:
            return jsonify({
                'success': False,
                'message': 'Could not understand the audio. Please try speaking more clearly.'
            })
        except sr.RequestError:
            return jsonify({
                'success': False,
                'message': 'Speech recognition service is unavailable.'
            })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing voice input.'
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Process text chat messages"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'success': False,
                'message': 'Please provide a message.'
            }), 400
        
        result = assistant.process_voice_command(message)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing your message.'
        }), 500

@app.route('/api/speak', methods=['POST'])
def speak_text():
    """Convert text to speech"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({
                'success': False,
                'message': 'Please provide text to speak.'
            }), 400
        
        # Speak in a separate thread to avoid blocking
        def speak_async():
            assistant.speak(text)
        
        thread = threading.Thread(target=speak_async)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Text is being spoken.'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'An error occurred while processing text-to-speech.'
        }), 500

@app.route('/api/status')
def status():
    """Get API status"""
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'weather': True,
            'voice_recognition': True,
            'text_to_speech': engine is not None,
            'chat': True
        }
    })

if __name__ == '__main__':
    print("🚀 Voice Assistant API Starting...")
    print("📡 Server will be available at: http://localhost:5000")
    print("🎤 Features: Weather, Voice Recognition, Text-to-Speech, Chat")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# For Vercel deployment
app = app
