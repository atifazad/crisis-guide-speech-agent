# Emergency Call Setup Guide

This guide explains how to set up real emergency calling functionality using Twilio and ACI.dev integration.

## Prerequisites

1. **Twilio Account**: Sign up at [twilio.com](https://www.twilio.com)
2. **ACI.dev Account**: Sign up at [aci.dev](https://www.aci.dev) (optional for enhanced features)
3. **Public Webhook URL**: Your server needs to be accessible from the internet for Twilio webhooks

## Setup Steps

### 1. Twilio Configuration

#### Get Twilio Credentials
1. Log into your Twilio Console
2. Copy your **Account SID** and **Auth Token**
3. Get a **Twilio Phone Number** for making calls

#### Configure Environment Variables
Add these to your `.env` file:

```bash
# Enable emergency calls
EMERGENCY_CALL_ENABLED=true

# Twilio credentials
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number_here

# Target phone number (your phone for testing)
EMERGENCY_TARGET_PHONE=+1234567890
```

### 2. ACI.dev Configuration (Optional)

#### Get ACI.dev Credentials
1. Sign up at [aci.dev](https://www.aci.dev)
2. Get your **API Key** and **Linked Account Owner ID**

#### Configure ACI.dev Environment Variables
Add these to your `.env` file:

```bash
# Enable ACI.dev integration
ACI_ENABLED=true

# ACI.dev credentials
ACI_API_KEY=your_aci_api_key_here
ACI_LINKED_ACCOUNT_OWNER_ID=your_linked_account_owner_id_here
```

### 3. Webhook Configuration

#### Set Up Public URL
Your server needs to be accessible from the internet. You can use:
- **ngrok**: `ngrok http 8001`
- **Cloudflare Tunnel**
- **VPS with public IP**

#### Configure Twilio Webhooks
1. Go to your Twilio Console
2. Navigate to Phone Numbers → Manage → Active numbers
3. Click on your Twilio phone number
4. Set the webhook URLs:
   - **Voice Configuration**: `https://your-domain.com/emergency-voice`
   - **Status Callback URL**: `https://your-domain.com/call-status`

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Test the Setup

Run the test script to verify everything is working:

```bash
python test_emergency_call.py
```

## How It Works

### Emergency Call Flow

1. **Emergency Detection**: The AI detects emergency keywords
2. **Protocol Initiation**: Emergency protocol starts with step-by-step guidance
3. **Call Initiation**: When escalation reaches step 4, a real call is made
4. **Call Monitoring**: The system monitors call status and provides updates
5. **ACI.dev Integration**: Optional logging and notifications via ACI.dev

### Emergency Call Types

- **Fire Emergency**: 4-step protocol with location confirmation
- **Medical Emergency**: 4-step protocol with symptom assessment
- **Danger/Threat**: 4-step protocol with safety assessment

### Call Features

- **Real Phone Calls**: Uses Twilio to make actual phone calls
- **Call Status Monitoring**: Tracks call progress in real-time
- **Emergency Logging**: Logs all emergency calls for compliance
- **ACI.dev Integration**: Enhanced logging and notifications

## Testing

### Test Emergency Call
1. Start the voice agent: `python src/agents/agentic_voice_agent.py`
2. Start the web UI: `python src/web/agentic_voice_web_ui.py`
3. Open the web interface: `http://localhost:8001`
4. Say "fire" or "emergency" to trigger emergency protocol
5. Follow the step-by-step guidance
6. The system will call your target phone number

### Test ACI.dev Integration
1. Enable ACI.dev in your `.env` file
2. Configure ACI.dev credentials
3. Emergency calls will automatically:
   - Log to Notion
   - Send SMS notifications
   - Create emergency documents

## Safety Features

### False Positive Prevention
- **Multiple Confirmations**: Requires user confirmation before calling
- **Timeout Protection**: Automatic escalation only after timeouts
- **User Override**: Users can cancel emergency calls

### Call Logging
- **Compliance Logs**: All calls logged to `emergency_calls.log`
- **Status Tracking**: Call status updates logged to `call_status.log`
- **ACI.dev Logging**: Enhanced logging via ACI.dev integrations

## Troubleshooting

### Common Issues

1. **Twilio Authentication Error**
   - Verify your Account SID and Auth Token
   - Check that your Twilio account is active

2. **Webhook Not Receiving Calls**
   - Ensure your server is publicly accessible
   - Verify webhook URLs in Twilio console
   - Check firewall settings

3. **ACI.dev Integration Not Working**
   - Verify your API key and linked account ID
   - Check that ACI.dev is enabled in configuration

### Debug Mode

Enable debug logging by setting:
```bash
LOG_LEVEL=DEBUG
```

## Security Considerations

### Emergency Call Safety
- **Test Mode**: Use simulation mode for testing
- **Target Phone**: Set your phone number for testing, not 911
- **Confirmation**: Always require user confirmation
- **Logging**: Comprehensive logging for audit trails

### Data Privacy
- **Local Storage**: Emergency logs stored locally
- **Secure Transmission**: Use HTTPS for webhooks
- **Access Control**: Limit access to emergency logs

## Production Deployment

### For Production Use
1. **Use Real Emergency Numbers**: Replace test phone with actual emergency numbers
2. **Enable ACI.dev**: For enhanced logging and notifications
3. **Secure Webhooks**: Use HTTPS and proper authentication
4. **Monitoring**: Set up monitoring for emergency call system
5. **Compliance**: Ensure compliance with local emergency calling regulations

### Legal Considerations
- **Emergency Call Regulations**: Check local laws about automated emergency calls
- **False Emergency Penalties**: Be aware of penalties for false emergency calls
- **User Consent**: Ensure users understand emergency call functionality
- **Data Retention**: Follow local data retention requirements

## Support

For issues with:
- **Twilio**: Contact Twilio support
- **ACI.dev**: Contact ACI.dev support
- **Emergency Call System**: Check logs and test scripts

## Emergency Call Logs

Emergency calls are logged in:
- `emergency_calls.log`: Emergency call details
- `call_status.log`: Call status updates
- Console output: Real-time call monitoring

Example log entry:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "call_id": "CA1234567890",
  "emergency_type": "fire",
  "location": "123 Main St",
  "situation": "Fire detected in kitchen",
  "status": "initiated"
}
``` 