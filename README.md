# Crisis Guide (Your Trusted Guide in any Emergency or Crisis Situation)

A simple and powerful command-line chat agent built with Python and OpenAI API. This agent can have natural conversations with users, maintain conversation history, and save/load conversations.

## Features

### Emergency Call System USING TWILLIO
- 🚨 **Real Emergency Calls**: Uses Twilio to make actual phone calls
- 🧠 **LLM-Driven Response**: AI dynamically assesses situations and determines appropriate actions
- 📞 **Intelligent Escalation**: Context-aware escalation based on user responsiveness
- 🔗 **ACI.dev Integration**: Enhanced logging and notifications
- 📊 **Call Status Monitoring**: Real-time call progress tracking
- 📝 **Compliance Logging**: Complete audit trail for emergency calls
- 🛡️ **Safety Features**: Permission-based emergency calls with user confirmation

### Voice Chat Agent
- 🎤 **Real-time Speech-to-Text**: Uses Google Whisper for accurate transcription
- 🔊 **High-quality Text-to-Speech**: Uses ElevenLabs for natural voice synthesis
- 🌐 **WebRTC Audio Streaming**: Real-time audio capture and playback
- 📱 **Modern Web Interface**: Beautiful, responsive voice chat interface
- 🎛️ **Volume Control**: Adjustable audio playback volume
- 📊 **Status Indicators**: Real-time processing status and feedback
- 🔄 **Dual Input Modes**: Voice recording or text input


### Text Chat Agent
- 🤖 **AI-Powered Conversations**: Uses OpenAI's GPT-4o for natural language processing
- 💬 **Conversation History**: Maintains context throughout the conversation
- 💾 **Save/Load Conversations**: Save conversations to JSON files and load them later
- 📊 **Conversation Analytics**: View statistics about your conversations
- 🛡️ **Error Handling**: Robust error handling for API issues and network problems
- 📝 **Logging**: Comprehensive logging for debugging and monitoring
- ⚡ **Real-time Responses**: Get instant responses from the AI assistant




## Installation

### Option 1: Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

### Option 2: Manual Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python test_agent.py
   ```

## Configuration

### Environment Variables

The application uses environment variables for configuration. The `.env` file has been created with the current API keys. For production use, you should update the API keys in the `.env` file with your own keys.

To use your own API keys, edit the `.env` file:

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-4o
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# ElevenLabs Configuration
ELEVENLABS_API_KEY=your_elevenlabs_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM (AI Personality)
ELEVENLABS_BASE_URL=https://api.elevenlabs.io/v1

# Whisper Configuration
WHISPER_MODEL=small
WHISPER_LANGUAGE=en

# Server Configuration
WEBSOCKET_PORT=8766
WEB_UI_PORT=8001

# Emergency Configuration
EMERGENCY_ESCALATION_DELAY=5
MAX_SILENCE_COUNT=3
PROACTIVE_CHECK_INTERVAL=2

# Twilio Configuration (for emergency calls)
EMERGENCY_CALL_ENABLED=true
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here
EMERGENCY_TARGET_PHONE=+1234567890

# ACI.dev Configuration (for enhanced integrations)
ACI_ENABLED=false
ACI_API_KEY=your_aci_api_key_here
ACI_LINKED_ACCOUNT_OWNER_ID=your_aci_linked_account_owner_id_here
```

### Required API Keys

1. **OpenAI API Key**: Get from [OpenAI Platform](https://platform.openai.com/)
2. **ElevenLabs API Key**: Get from [ElevenLabs](https://elevenlabs.io/)
3. **Twilio Account** (for emergency calls): Get from [Twilio](https://www.twilio.com/)
4. **ACI.dev Account** (optional): Get from [ACI.dev](https://www.aci.dev/)

## Emergency Call Setup

For emergency calling functionality, see the detailed setup guide: [EMERGENCY_CALL_SETUP.md](EMERGENCY_CALL_SETUP.md)

**Quick Setup:**
1. Sign up for Twilio and get your credentials
2. Add Twilio configuration to your `.env` file
3. Set up webhook URLs in Twilio console
4. Test with `python test_emergency_call.py`

## LLM-Driven Emergency Response

The system now uses AI to dynamically assess emergency situations and determine the most appropriate response:

### How It Works

1. **Emergency Detection**: The system detects emergency keywords in user input
2. **LLM Assessment**: The AI analyzes the situation and determines the best course of action
3. **Dynamic Response**: Responses are generated based on context, not rigid protocols
4. **Intelligent Escalation**: Escalation occurs based on user responsiveness and situation severity
5. **Permission-Based Calls**: Emergency services are only called with explicit user permission

### Key Features

- **Context-Aware**: AI considers the specific emergency type and user input
- **Flexible Protocols**: No rigid step-by-step procedures - AI adapts to the situation
- **Safety-First**: Always prioritizes immediate safety before gathering details
- **User Control**: Emergency calls require explicit user confirmation
- **Intelligent Escalation**: Escalation timing and content adapts to the situation

### Emergency Types Supported

- **Fire Emergencies**: Fire detection, evacuation guidance, location assessment
- **Medical Emergencies**: Consciousness checks, symptom assessment, medical guidance
- **Danger/Threat Situations**: Safety assessment, threat evaluation, location confirmation
- **General Emergencies**: Flexible response for various emergency scenarios

## Usage

### Basic Usage

#### Text Chat Agent
Run the text chat agent:
```bash
python chat_agent.py
```

#### Voice Chat Agent
1. **Setup voice components**:
   ```bash
   ./setup_voice.sh
   ```

2. **Configure API keys** (see Configuration section above)

3. **Start the voice server** (Terminal 1):
   ```bash
   python src/agents/agentic_voice_agent.py
   ```

4. **Start the web interface** (Terminal 2):
   ```bash
   python src/web/agentic_voice_web_ui.py
   ```

5. **Open in browser**:
   ```
   http://localhost:8001
   ```

### Quick Start with Script

Use the provided startup script to run both services:

```bash
./start_agentic_voice.sh
```

This will:
- Check port availability
- Validate configuration
- Start both the WebSocket server and web UI
- Display connection information

### Available Commands

Once the chat agent is running, you can use these special commands:

- `quit` - Exit the chat agent
- `clear` - Clear the conversation history
- `save` - Save the current conversation to a JSON file
- `load <filename>` - Load a previous conversation from a JSON file
- `summary` - Show conversation statistics

### Example Session

```
🤖 Text Chat Agent
==================================================
Type 'quit' to exit, 'clear' to clear history, 'save' to save conversation
Type 'load <filename>' to load a previous conversation
Type 'summary' to see conversation statistics
==================================================

✅ Chat agent initialized successfully!

💬 Start chatting with the AI assistant...

👤 You: Hello! How are you today?
🤖 Assistant: Hello! I'm doing well, thank you for asking. I'm here and ready to help you with any questions or tasks you might have. How can I assist you today?

👤 You: Can you help me write a Python function?
🤖 Assistant: Of course! I'd be happy to help you write a Python function. What kind of function do you need? Please let me know:

1. What the function should do
2. What parameters it should take
3. What it should return
4. Any specific requirements or constraints

For example, are you looking to create a function that:
- Performs calculations?
- Processes data?
- Handles file operations?
- Something else entirely?

Once you give me the details, I can help you write the function and explain how it works!

👤 You: summary
📊 Conversation Summary:
   Total messages: 4
   User messages: 2
   Assistant messages: 2
   Total user characters: 47
   Total assistant characters: 234

👤 You: save
💾 Conversation saved to conversation_20241201_143022.json

👤 You: quit
👋 Goodbye!
```

## Model Selection

By default, the agent uses `gpt-4o`. You can change this by modifying the `OPENAI_MODEL` environment variable.

Available models:
- `gpt-4o` (default, latest and most capable model)
- `gpt-4-turbo` (previous GPT-4 model)
- `gpt-3.5-turbo` (fast and cost-effective)


## Architecture

### Service Layer

The application uses a service-oriented architecture with dedicated services for each external API:

- **`OpenAIService`**: Handles all OpenAI API interactions including GPT-4o responses
- **`ElevenLabsService`**: Handles text-to-speech conversion and voice management
- **`WhisperService`**: Handles speech-to-text transcription

Each service provides:
- **Error handling and retries**
- **API key validation**
- **Configuration management**
- **Logging and monitoring**

### Benefits of Service Layer

- **Separation of concerns**: Each service handles one specific API
- **Better error handling**: Centralized error handling per service
- **Easier testing**: Can mock individual services for testing
- **Reusability**: Services can be used by other components
- **Maintainability**: Changes to API logic are isolated

## Features in Detail

### Conversation Management

The chat agent maintains a complete conversation history, allowing for contextual responses. Each message includes:
- Role (user/assistant)
- Content
- Timestamp

### Error Handling

The agent handles various error scenarios:
- **Authentication errors**: Invalid API key
- **Rate limiting**: Too many requests
- **Network issues**: Connection problems
- **API errors**: OpenAI service issues

### Logging

All activities are logged to both:
- Console output
- `chat_agent.log` file

### Conversation Persistence

Conversations can be saved and loaded using JSON format, preserving:
- All messages
- Timestamps
- Conversation context

## Troubleshooting

### Common Issues

1. **"Configuration validation failed"**
   - Check that your `.env` file exists and contains valid API keys
   - Ensure both `OPENAI_API_KEY` and `ELEVENLABS_API_KEY` are set
   - Copy `env.example` to `.env` and update with your keys

2. **"Authentication failed"**
   - Check if the API key is correct
   - Ensure the API key has sufficient credits

3. **"Rate limit exceeded"**
   - Wait a moment and try again
   - Consider upgrading your OpenAI plan

4. **"Module not found" errors**
   - Run `pip install -r requirements.txt`
   - Ensure you're using Python 3.7+

5. **Permission errors when saving files**
   - Check write permissions in the current directory
   - Try running from a different location

### Getting Help

If you encounter issues:
1. Check the `chat_agent.log` file for detailed error messages
2. Verify your internet connection
3. Ensure your API keys are valid and have credits
4. Check that all environment variables are properly set

## Security Notes

- API keys are now stored in environment variables (`.env` file)
- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- Consider using `.env` files for sensitive data in production

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the chat agent! 