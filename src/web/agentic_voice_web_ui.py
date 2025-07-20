#!/usr/bin/env python3
"""
Agentic Voice Chat Agent Web UI
AI that takes complete control of conversations with emergency monitoring
"""

import json
import logging
from datetime import datetime
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Agentic Voice Chat Agent",
    description="AI that takes complete control of conversations with emergency monitoring",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def get_agentic_voice_interface():
    """Serve the agentic voice chat interface."""
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Your Trusted Guide in Times of Crisis</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
        <style>
            body {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                min-height: 100vh;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .agentic-voice-container {
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                margin: 20px auto;
                max-width: 900px;
                height: 90vh;
                display: flex;
                flex-direction: column;
            }
            .agentic-voice-header {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
                padding: 20px;
                border-radius: 20px 20px 0 0;
                text-align: center;
            }
            .emergency-indicator {
                background: #ffc107;
                color: #212529;
                padding: 10px;
                border-radius: 10px;
                margin: 10px 0;
                text-align: center;
                font-weight: bold;
                animation: pulse 2s infinite;
            }
            .agentic-voice-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }
            .message {
                margin-bottom: 15px;
                display: flex;
                align-items: flex-start;
            }
            .message.user {
                justify-content: flex-end;
            }
            .message.assistant {
                justify-content: flex-start;
            }
            .message-content {
                max-width: 70%;
                padding: 12px 16px;
                border-radius: 18px;
                word-wrap: break-word;
            }
            .message.user .message-content {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
            }
            .message.assistant .message-content {
                background: white;
                border: 1px solid #e9ecef;
                color: #333;
            }
            .message.assistant.emergency .message-content {
                background: #fff3cd;
                border: 2px solid #ffc107;
                color: #856404;
                font-weight: bold;
            }
            .message-avatar {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 10px;
                font-size: 18px;
            }
            .user-avatar {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
            }
            .assistant-avatar {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
            }
            .assistant-avatar.emergency {
                background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
                color: #212529;
            }
            .agentic-voice-controls {
                padding: 20px;
                background: white;
                border-radius: 0 0 20px 20px;
                border-top: 1px solid #e9ecef;
            }
            .voice-button {
                width: 80px;
                height: 80px;
                border-radius: 50%;
                border: none;
                font-size: 24px;
                margin: 10px;
                transition: all 0.3s ease;
                cursor: pointer;
            }
            .btn-record {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
            }
            .btn-record:hover {
                transform: scale(1.1);
                box-shadow: 0 5px 15px rgba(220, 53, 69, 0.4);
            }
            .btn-record.recording {
                background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
                animation: pulse 1s infinite;
            }
            .btn-record.emergency {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                animation: emergency-pulse 0.5s infinite;
            }
            .status-indicator {
                margin: 10px 0;
                padding: 10px;
                border-radius: 10px;
                background: #e9ecef;
                color: #666;
                font-size: 14px;
            }
            .status-emergency {
                background: #f8d7da;
                color: #721c24;
                border: 2px solid #dc3545;
            }
            .status-monitoring {
                background: #fff3cd;
                color: #856404;
            }
            .status-processing {
                background: #d1ecf1;
                color: #0c5460;
            }
            .controls {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                justify-content: center;
                flex-wrap: wrap;
            }
            .btn-control {
                padding: 8px 16px;
                border-radius: 20px;
                border: none;
                font-size: 14px;
                transition: all 0.3s ease;
            }
            .btn-clear {
                background: #6c757d;
                color: white;
            }

            .btn-control:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
            }
            .text-input {
                margin-top: 15px;
                display: flex;
                gap: 10px;
            }
            .form-control {
                border-radius: 25px;
                border: 2px solid #e9ecef;
                padding: 12px 20px;
                font-size: 16px;
                flex: 1;
            }
            .btn-send {
                border-radius: 25px;
                padding: 12px 20px;
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                border: none;
                color: white;
                font-size: 16px;
            }
            .typing-indicator {
                display: none;
                padding: 12px 16px;
                background: white;
                border: 1px solid #e9ecef;
                border-radius: 18px;
                margin: 10px 0;
                color: #666;
                font-style: italic;
            }
            .volume-control {
                margin: 15px 0;
                text-align: center;
            }
            .volume-slider {
                width: 200px;
                margin: 0 10px;
            }
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            @keyframes emergency-pulse {
                0% { transform: scale(1); box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.7); }
                70% { transform: scale(1.05); box-shadow: 0 0 0 10px rgba(220, 53, 69, 0); }
                100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(220, 53, 69, 0); }
            }
            .emergency-features {
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                color: white;
                padding: 15px;
                border-radius: 15px;
                margin-bottom: 15px;
                text-align: center;
            }
        </style>
    </head>
    <body>
        <div class="container-fluid">
            <div class="agentic-voice-container">
                <div class="agentic-voice-header">
                    <h2><i class="fas fa-exclamation-triangle"></i> Your Trusted Guide in Times of Crisis</h2>
                    <p class="mb-0">AI that takes COMPLETE CONTROL with emergency monitoring! 🚨</p>
                </div>
                
                <div class="emergency-features">
                    <strong>🚨 EMERGENCY FEATURES:</strong> Automatic detection • Proactive monitoring • Emergency escalation • Complete control
                </div>
                
                <div class="agentic-voice-messages" id="agenticVoiceMessages">
                    <div class="message assistant">
                        <div class="message-avatar assistant-avatar">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="message-content">
                            Hello! I'm your agentic voice assistant. I'm here to take complete control of our conversation and ensure your safety. If you mention any emergency, I will immediately take action. What's happening? 🚨
                        </div>
                    </div>
                </div>
                
                <div class="typing-indicator" id="typingIndicator">
                    <i class="fas fa-circle"></i>
                    <i class="fas fa-circle"></i>
                    <i class="fas fa-circle"></i>
                    AI is taking control...
                </div>
                
                <div class="agentic-voice-controls">
                    <div class="controls">
                        <button class="btn-control btn-clear" onclick="clearChat()">
                            <i class="fas fa-trash"></i> Clear
                        </button>
                    </div>
                    
                    <div class="status-indicator" id="statusIndicator" style="display: none;">
                        <i class="fas fa-info-circle"></i> <span id="statusText">Monitoring conversation...</span>
                    </div>
                    
                    <div class="volume-control">
                        <label for="volumeSlider">Volume: </label>
                        <input type="range" id="volumeSlider" class="volume-slider" min="0" max="1" step="0.1" value="0.8">
                        <span id="volumeValue">80%</span>
                    </div>
                    
                    <button class="voice-button btn-record" id="recordButton" onclick="toggleRecording()">
                        <i class="fas fa-microphone"></i>
                    </button>
                    
                    <div class="text-input">
                        <input type="text" class="form-control" id="textInput" 
                               placeholder="Type your message or say 'help' for emergency..." 
                               onkeypress="handleKeyPress(event)">
                        <button class="btn btn-send" onclick="sendTextMessage()">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        
        <script>
            let websocket = null;
            let mediaRecorder = null;
            let audioChunks = [];
            let isRecording = false;
            let isConnected = false;
            let emergencyMode = false;
            
            // Initialize WebSocket connection
            function connectWebSocket() {
                websocket = new WebSocket('ws://localhost:8766');
                
                websocket.onopen = function(event) {
                    console.log('WebSocket connected');
                    isConnected = true;
                    updateStatus('Connected to agentic voice server', 'processing');
                };
                
                websocket.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleWebSocketMessage(data);
                };
                
                websocket.onclose = function(event) {
                    console.log('WebSocket disconnected');
                    isConnected = false;
                    updateStatus('Disconnected from voice server', 'emergency');
                };
                
                websocket.onerror = function(error) {
                    console.error('WebSocket error:', error);
                    updateStatus('Connection error', 'emergency');
                };
            }
            
            function handleWebSocketMessage(data) {
                switch(data.type) {
                    case 'transcript':
                        addMessage(data.text, 'user');
                        updateStatus('Transcription received', 'processing');
                        break;
                    case 'response_text':
                        const isEmergency = emergencyMode || data.text.toLowerCase().includes('emergency') || 
                                          data.text.toLowerCase().includes('fire') || 
                                          data.text.toLowerCase().includes('help');
                        addMessage(data.text, 'assistant', isEmergency);
                        updateStatus('Response received', isEmergency ? 'emergency' : 'processing');
                        break;
                    case 'audio_response':
                        playAudioResponse(data.audio);
                        updateStatus('Playing audio response', 'processing');
                        break;
                    case 'status':
                        updateStatus(data.message, 'processing');
                        break;
                    case 'error':
                        updateStatus(data.message, 'emergency');
                        break;
                    case 'pong':
                        // Keep connection alive
                        break;
                }
            }
            
            function updateStatus(message, type) {
                const indicator = document.getElementById('statusIndicator');
                const statusText = document.getElementById('statusText');
                
                indicator.className = `status-indicator status-${type}`;
                statusText.textContent = message;
                indicator.style.display = 'block';
                
                // Update emergency mode
                if (type === 'emergency') {
                    emergencyMode = true;
                    document.getElementById('recordButton').classList.add('emergency');
                } else {
                    emergencyMode = false;
                    document.getElementById('recordButton').classList.remove('emergency');
                }
                
                setTimeout(() => {
                    if (type !== 'emergency') {
                        indicator.style.display = 'none';
                    }
                }, 3000);
            }
            
            async function toggleRecording() {
                if (!isConnected) {
                    updateStatus('Not connected to voice server', 'emergency');
                    return;
                }
                
                if (isRecording) {
                    stopRecording();
                } else {
                    startRecording();
                }
            }
            
            async function startRecording() {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);
                    audioChunks = [];
                    
                    mediaRecorder.ondataavailable = function(event) {
                        audioChunks.push(event.data);
                    };
                    
                    mediaRecorder.onstop = function() {
                        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                        sendAudioToServer(audioBlob);
                    };
                    
                    mediaRecorder.start();
                    isRecording = true;
                    
                    const recordButton = document.getElementById('recordButton');
                    recordButton.classList.add('recording');
                    recordButton.innerHTML = '<i class="fas fa-stop"></i>';
                    
                    updateStatus('Recording... Click to stop', 'processing');
                    
                } catch (error) {
                    console.error('Error starting recording:', error);
                    updateStatus('Error accessing microphone', 'emergency');
                }
            }
            
            function stopRecording() {
                if (mediaRecorder && isRecording) {
                    mediaRecorder.stop();
                    mediaRecorder.stream.getTracks().forEach(track => track.stop());
                    isRecording = false;
                    
                    const recordButton = document.getElementById('recordButton');
                    recordButton.classList.remove('recording');
                    recordButton.innerHTML = '<i class="fas fa-microphone"></i>';
                    
                    updateStatus('Processing audio...', 'processing');
                }
            }
            
            function sendAudioToServer(audioBlob) {
                const reader = new FileReader();
                reader.onload = function() {
                    const base64Audio = reader.result.split(',')[1];
                    
                    if (websocket && websocket.readyState === WebSocket.OPEN) {
                        websocket.send(JSON.stringify({
                            type: 'audio',
                            audio: base64Audio
                        }));
                    }
                };
                reader.readAsDataURL(audioBlob);
            }
            
            function sendTextMessage() {
                const textInput = document.getElementById('textInput');
                const message = textInput.value.trim();
                
                if (!message || !isConnected) return;
                
                addMessage(message, 'user');
                textInput.value = '';
                
                if (websocket && websocket.readyState === WebSocket.OPEN) {
                    websocket.send(JSON.stringify({
                        type: 'text',
                        text: message
                    }));
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendTextMessage();
                }
            }
            
            function addMessage(content, sender, isEmergency = false) {
                const agenticVoiceMessages = document.getElementById('agenticVoiceMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}`;
                
                const avatar = document.createElement('div');
                avatar.className = `message-avatar ${sender}-avatar`;
                if (isEmergency && sender === 'assistant') {
                    avatar.classList.add('emergency');
                }
                avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
                
                const messageContent = document.createElement('div');
                messageContent.className = 'message-content';
                if (isEmergency && sender === 'assistant') {
                    messageContent.classList.add('emergency');
                }
                messageContent.textContent = content;
                
                messageDiv.appendChild(avatar);
                messageDiv.appendChild(messageContent);
                agenticVoiceMessages.appendChild(messageDiv);
                
                agenticVoiceMessages.scrollTop = agenticVoiceMessages.scrollHeight;
            }
            
            function playAudioResponse(base64Audio) {
                const audio = new Audio(`data:audio/mpeg;base64,${base64Audio}`);
                const volumeSlider = document.getElementById('volumeSlider');
                audio.volume = parseFloat(volumeSlider.value);
                audio.play();
            }
            
            function clearChat() {
                if (confirm('Are you sure you want to clear the conversation?')) {
                    const agenticVoiceMessages = document.getElementById('agenticVoiceMessages');
                    agenticVoiceMessages.innerHTML = `
                        <div class="message assistant">
                            <div class="message-avatar assistant-avatar">
                                <i class="fas fa-robot"></i>
                            </div>
                            <div class="message-content">
                                Hello! I'm your agentic voice assistant. I'm here to take complete control of our conversation and ensure your safety. If you mention any emergency, I will immediately take action. What's happening? 🚨
                            </div>
                        </div>
                    `;
                    emergencyMode = false;
                    updateStatus('Conversation cleared', 'processing');
                }
            }
            

            
            // Volume control
            document.getElementById('volumeSlider').addEventListener('input', function() {
                const volumeValue = document.getElementById('volumeValue');
                volumeValue.textContent = Math.round(this.value * 100) + '%';
            });
            
            // Initialize connection when page loads
            window.onload = function() {
                connectWebSocket();
            };
        </script>
    </body>
    </html>
    """

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "agentic-voice-web-ui"}

if __name__ == "__main__":
    import uvicorn
    from config import Config
    
    # Validate configuration
    if not Config.validate_config():
        logger.error("Configuration validation failed. Please check your environment variables.")
        exit(1)
    
    uvicorn.run(
        "agentic_voice_web_ui:app",
        host="0.0.0.0",
        port=Config.get_web_ui_port(),
        reload=True
    ) 