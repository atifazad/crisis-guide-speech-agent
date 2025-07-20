#!/bin/bash

# Agentic Voice Agent Startup Script
# Runs both the WebSocket server and web UI concurrently

echo "🚨 Starting Agentic Voice Agent..."
echo "=================================="

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not detected. Activating..."
    source .venv/bin/activate
fi

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Get ports from Python config
WEBSOCKET_PORT=$(python -c "from config import Config; print(Config.get_websocket_port())")
WEB_UI_PORT=$(python -c "from config import Config; print(Config.get_web_ui_port())")

# Check if ports are available
echo "🔍 Checking port availability..."
if ! check_port $WEBSOCKET_PORT; then
    echo "Please stop any service using port $WEBSOCKET_PORT"
    exit 1
fi

if ! check_port $WEB_UI_PORT; then
    echo "Please stop any service using port $WEB_UI_PORT"
    exit 1
fi

echo ""
echo "🎤 Starting Agentic Voice WebSocket Server (Port $WEBSOCKET_PORT)..."
python src/agents/agentic_voice_agent.py &
VOICE_PID=$!

echo "🌐 Starting Agentic Voice Web UI (Port $WEB_UI_PORT)..."
python src/web/agentic_voice_web_ui.py &
WEB_PID=$!

echo ""
echo "✅ Agentic Voice Agent started successfully!"
echo "=========================================="
echo "🎤 Voice Server: ws://localhost:$WEBSOCKET_PORT"
echo "🌐 Web UI: http://localhost:$WEB_UI_PORT"
echo ""
echo "🚨 EMERGENCY FEATURES:"
echo "   • Automatic emergency detection"
echo "   • Proactive monitoring"
echo "   • Emergency escalation"
echo "   • Complete conversation control"
echo ""
echo "💡 Test Emergency: Click 'Test Emergency' button in the web UI"
echo "🎤 Voice Commands: Click the microphone button to speak"
echo "📝 Text Input: Type messages in the text field"
echo ""
echo "Press Ctrl+C to stop all services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping Agentic Voice Agent..."
    kill $VOICE_PID 2>/dev/null
    kill $WEB_PID 2>/dev/null
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait 