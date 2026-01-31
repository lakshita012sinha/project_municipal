# SMS Integration Setup Guide

## Overview
This guide will help you set up real SMS delivery for OTP verification in your Django application. We support three major SMS providers:

1. **MSG91** (Recommended for India) - Cost-effective, reliable
2. **Twilio** (International) - Premium service, global coverage
3. **TextLocal** (India) - Good for Indian market

## Quick Setup (Recommended: MSG91)

### Step 1: Sign up for MSG91
1. Go to [https://msg91.com/](https://msg91.com/)
2. Sign up for a free account
3. Verify your mobile number and email
4. You'll get free credits to start with

### Step 2: Get Your API Credentials
1. Login to MSG91 dashboard
2. Go to **API** section or visit [https://control.msg91.com/user/index.php#api](https://control.msg91.com/user/index.php#api)
3. Copy your **Auth Key**

### Step 3: Configure Django Settings
Open `Rajasthan_Municipal/Rajasthan_Municipal/settings.py` and update:

```python
# Replace 'your_msg91_auth_key_here' with your actual Auth Key
MSG91_AUTH_KEY = 'your_actual_auth_key_from_msg91'

# Optional: Change sender ID (6 characters max)
MSG91_SENDER_ID = 'RAJMUN'  # or keep 'OTPSMS'
```

### Step 4: Test the Integration
1. Run your Django server: `python manage.py runserver`
2. Register a user with your real mobile number
3. Try logging in - you should receive an actual SMS!

## Alternative Setup Options

### Option 2: Twilio (International)

1. **Sign up**: [https://www.twilio.com/](https://www.twilio.com/)
2. **Get credentials** from [Twilio Console](https://console.twilio.com/)
3. **Buy a phone number** (required for sending SMS)
4. **Update settings.py**:
```python
DEFAULT_SMS_PROVIDER = 'twilio'
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'  # Your Twilio number
```
5. **Install Twilio**: `pip install twilio`

### Option 3: TextLocal (India)

1. **Sign up**: [https://www.textlocal.in/](https://www.textlocal.in/)
2. **Get API key** from [API section](https://www.textlocal.in/user/index/api)
3. **Update settings.py**:
```python
DEFAULT_SMS_PROVIDER = 'textlocal'
TEXTLOCAL_API_KEY = 'your_api_key'
TEXTLOCAL_SENDER = 'RAJMUN'  # 6 characters max
```

## Testing Your Setup

### Method 1: Through Web Interface
1. Start Django server: `python manage.py runserver`
2. Go to registration page: `http://127.0.0.1:8000/register/`
3. Register with your real mobile number
4. Try logging in - check if SMS arrives

### Method 2: Django Shell Testing
```python
python manage.py shell

# Test SMS sending
from users.sms_services import send_otp_sms
result = send_otp_sms('+919876543210', '123456')
print(result)
```

## Troubleshooting

### Common Issues:

1. **"SMS service configuration error"**
   - Check if you've added the correct API keys in settings.py
   - Ensure no typos in the configuration

2. **"Network error" or timeout**
   - Check your internet connection
   - Verify the SMS provider's service status

3. **SMS not received**
   - Check if the mobile number format is correct (+91xxxxxxxxxx for India)
   - Verify you have credits in your SMS provider account
   - Check spam/promotional SMS folder

4. **"Invalid credentials" error**
   - Double-check your API keys
   - Ensure your SMS provider account is active

### Debug Mode:
Check the console output and `sms.log` file for detailed error messages.

## Cost Comparison (Approximate)

| Provider | Cost per SMS (India) | Free Credits | Best For |
|----------|---------------------|--------------|----------|
| MSG91 | ₹0.15-0.25 | Yes (₹20-50) | India, Cost-effective |
| Twilio | ₹0.50-1.00 | Yes ($15) | International, Premium |
| TextLocal | ₹0.20-0.30 | Yes (₹20) | India, Good support |

## Production Recommendations

1. **For India-only**: Use MSG91 or TextLocal
2. **For International**: Use Twilio
3. **For High Volume**: MSG91 (better rates)
4. **For Premium Features**: Twilio (delivery reports, etc.)

## Security Notes

- Never commit API keys to version control
- Use environment variables in production:
```python
import os
MSG91_AUTH_KEY = os.environ.get('MSG91_AUTH_KEY')
```
- Monitor SMS usage to prevent abuse
- Implement rate limiting for OTP requests

## Support

If you face issues:
1. Check the `sms.log` file for errors
2. Test with Django shell first
3. Verify your SMS provider account status
4. Check mobile number format

The system automatically tries fallback providers if the primary one fails, ensuring maximum reliability.