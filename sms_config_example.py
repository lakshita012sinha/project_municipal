"""
SMS Service Configuration Example
Add these settings to your Django settings.py file

🆓 FREE TESTING: The app is already configured with a free simulation service!
Just run the server and check console output for OTP codes.
"""

# =============================================================================
# SMS SERVICE CONFIGURATION
# =============================================================================

# Choose your SMS provider: 'free', 'fast2sms', 'way2sms', 'msg91', 'twilio', or 'textlocal'
# 'free' = Console simulation (no setup needed, unlimited)
# 'fast2sms' = Real SMS with 100 free messages
# 'msg91' = Professional service with free credits
DEFAULT_SMS_PROVIDER = 'free'

# =============================================================================
# FREE SIMULATION SERVICE (Already Configured - No Setup Needed!)
# =============================================================================
# This displays OTP in console output and logs
# Perfect for development and testing
SMS_TEST_MODE = True
SMS_TEST_NUMBERS = ['+919876543210', '+919123456789']  # Add your test numbers

# =============================================================================
# FAST2SMS Configuration (100 Free SMS)
# =============================================================================
# Sign up at: https://www.fast2sms.com/ (Free account gives 100 SMS)
# Get API key from: Dashboard → API Keys
FAST2SMS_API_KEY = 'your_fast2sms_api_key_here'
FAST2SMS_SENDER_ID = 'FSTSMS'

# =============================================================================
# WAY2SMS Configuration (Free Service)
# =============================================================================
# Sign up at: https://www.way2sms.com/
WAY2SMS_API_KEY = 'your_way2sms_api_key_here'
WAY2SMS_SECRET = 'your_way2sms_secret_here'

# =============================================================================
# MSG91 Configuration (Recommended for India)
# =============================================================================
# Sign up at: https://msg91.com/
# Get your Auth Key from: https://control.msg91.com/user/index.php#api
MSG91_AUTH_KEY = 'your_msg91_auth_key_here'
MSG91_SENDER_ID = 'OTPSMS'  # 6 characters sender ID
MSG91_ROUTE = '4'  # 4 for transactional SMS

# =============================================================================
# Twilio Configuration (International)
# =============================================================================
# Sign up at: https://www.twilio.com/
# Get credentials from: https://console.twilio.com/
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token_here'
TWILIO_PHONE_NUMBER = '+1234567890'  # Your Twilio phone number

# =============================================================================
# TextLocal Configuration (India)
# =============================================================================
# Sign up at: https://www.textlocal.in/
# Get API key from: https://www.textlocal.in/user/index/api
TEXTLOCAL_API_KEY = 'your_textlocal_api_key_here'
TEXTLOCAL_SENDER = 'TXTLCL'  # 6 characters sender ID

# =============================================================================
# LOGGING CONFIGURATION (Optional)
# =============================================================================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'sms.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'users.sms_services': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}