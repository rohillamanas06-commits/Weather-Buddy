# Weather Buddy 🌤️

A voice-enabled weather assistant web application built with Flask that provides real-time weather information through both voice commands and web interface.

## Features

- 🎤 **Voice Recognition** - Speak your weather queries naturally
- 🔊 **Text-to-Speech** - Get weather updates spoken back to you
- 🌍 **Global Weather Data** - Get weather for any city worldwide
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🎨 **Modern UI** - Clean and intuitive user interface
- ⚡ **Real-time Updates** - Live weather data from OpenWeatherMap API

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Speech Recognition**: SpeechRecognition library
- **Text-to-Speech**: pyttsx3
- **Weather API**: OpenWeatherMap
- **Deployment**: Vercel/Netlify ready

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/weather-buddy.git
   cd weather-buddy
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Get OpenWeatherMap API Key**
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api)
   - Get your free API key
   - Replace the API key in `app.py` (line 16) or set as environment variable

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:5000`

## Usage

### Voice Commands
- Click the microphone button and say:
  - "What's the weather in New York?"
  - "Tell me about weather in London"
  - "How's the weather today in Tokyo?"

### Web Interface
- Type city name in the search box
- Click "Get Weather" button
- View detailed weather information

## API Endpoints

- `GET /` - Main application page
- `POST /weather` - Get weather data for a city
- `POST /voice-command` - Process voice commands
- `POST /speak` - Convert text to speech

## Weather Information Provided

- 🌡️ Current temperature
- 🌤️ Weather description
- 💧 Humidity levels
- 💨 Wind speed and direction
- 👁️ Visibility
- 🌅 Sunrise and sunset times

## Deployment

### Vercel
The project includes `vercel.json` configuration for easy deployment:
```bash
vercel --prod
```

### Netlify
The project includes `netlify.toml` configuration:
```bash
netlify deploy --prod
```

## Configuration

### Environment Variables
- `WEATHER_API_KEY` - Your OpenWeatherMap API key
- `FLASK_ENV` - Set to 'production' for deployment

### Voice Settings
The application automatically configures voice settings:
- Speech rate: 150 WPM
- Volume: 80%
- Voice: System default (female voice preferred)

## Browser Compatibility

- ✅ Chrome (recommended for voice features)
- ✅ Firefox
- ✅ Safari
- ✅ Edge

**Note**: Voice recognition works best in Chrome due to Web Speech API support.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for weather data API
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for voice input
- [pyttsx3](https://pypi.org/project/pyttsx3/) for text-to-speech functionality

## Support

If you encounter any issues or have questions:
1. Check the [Issues](https://github.com/yourusername/weather-buddy/issues) page
2. Create a new issue with detailed description
3. Include your browser and OS information

---

Made with ❤️ by Manas Rohilla 
