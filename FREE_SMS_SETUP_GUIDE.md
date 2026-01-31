# Free SMS Services Setup Guide

## 🆓 **Free SMS Options for Testing OTP**

I've implemented multiple free SMS services so you can test OTP functionality without any cost. Here are your options:

## Option 1: Free Simulation Service (Recommended for Testing) ⭐

**✅ Completely Free | ✅ No Registration | ✅ Works Immediately**

This is already configured and working! The OTP will be displayed in:
- Console output (where you run `python manage.py runserver`)
- Log file (`sms.log`)
- Django admin logs

### How to use:
1. **Already configured** - No setup needed!
2. **Start your server**: `python manage.py runserver`
3. **Register/Login** with any mobile number
4. **Check console** for the OTP code
5. **Enter OTP** in the verification page

### Test it now:
```bash
python manage.py test_sms +919876543210 --provider free
```

## Option 2: Fast2SMS (Free Tier) 🚀

**✅ 100 Free SMS | ✅ Real SMS Delivery | ✅ Easy Setup**

### Setup Steps:
1. **Sign up**: Go to [https://www.fast2sms.com/](https://www.fast2sms.com/)
2. **Verify mobile**: Complete phone verification
3. **Get API Key**: Go to Dashboard → API Keys
4. **Update settings**: In `settings.py`, replace:
   ```python
   DEFAULT_SMS_PROVIDER = 'fast2sms'
   FAST2SMS_API_KEY = 'your_actual_api_key_here'
   ```

### Test it:
```bash
python manage.py test_sms +919876543210 --provider fast2sms
```

## Option 3: Way2SMS (Free Service) 📱

**✅ Free SMS | ✅ Indian Service | ✅ Good for Testing**

### Setup Steps:
1. **Sign up**: Go to [https://www.way2sms.com/](https://www.way2sms.com/)
2. **Get credentials**: From API section
3. **Update settings**: In `settings.py`, replace:
   ```python
   DEFAULT_SMS_PROVIDER = 'way2sms'
   WAY2SMS_API_KEY = 'your_api_key'
   WAY2SMS_SECRET = 'your_secret'
   ```

## Option 4: MSG91 (Free Credits) 💳

**✅ ₹20-50 Free Credits | ✅ Professional Service | ✅ Reliable**

### Setup Steps:
1. **Sign up**: [https://msg91.com/](https://msg91.com/)
2. **Get free credits**: Verify account for free credits
3. **Get Auth Key**: From API section
4. **Update settings**:
   ```python
   DEFAULT_SMS_PROVIDER = 'msg91'
   MSG91_AUTH_KEY = 'your_auth_key'
   ```

## 🚀 **Quick Start (Zero Setup)**

The app is already configured to work with **Free Simulation Service**:

1. **Run the server**:
   ```bash
   cd Rajasthan_Municipal
   python manage.py runserver
   ```

2. **Register a user**: Go to `http://127.0.0.1:8000/register/`

3. **Try logging in**: Go to `http://127.0.0.1:8000/login/`

4. **Check console output** for OTP like this:
   ```
   ============================================================
   📱 FREE SMS SERVICE - OTP SENT
   ============================================================
   📞 Mobile Number: +919876543210
   🔐 OTP Code: 123456
   💬 Message: Your OTP for Rajasthan Municipal login is 123456...
   ⏰ Timestamp: 2024-01-30 10:30:45
   ============================================================
   ```

5. **Enter the OTP** in the verification page

## 🧪 **Testing Commands**

Test different providers:
```bash
# Test free simulation (no setup needed)
python manage.py test_sms +919876543210 --provider free

# Test Fast2SMS (after setup)
python manage.py test_sms +919876543210 --provider fast2sms

# Test Way2SMS (after setup)
python manage.py test_sms +919876543210 --provider way2sms

# Test MSG91 (after setup)
python manage.py test_sms +919876543210 --provider msg91
```

## 📊 **Comparison of Free Options**

| Service | Setup Time | Real SMS | Free Limit | Best For |
|---------|------------|----------|------------|----------|
| **Free Simulation** | 0 min | ❌ | Unlimited | Development/Testing |
| **Fast2SMS** | 5 min | ✅ | 100 SMS | Real testing |
| **Way2SMS** | 10 min | ✅ | Limited | Basic testing |
| **MSG91** | 5 min | ✅ | ₹20-50 credits | Production ready |

## 🔧 **Switching Between Services**

Change the provider in `settings.py`:
```python
# For free simulation (default)
DEFAULT_SMS_PROVIDER = 'free'

# For Fast2SMS
DEFAULT_SMS_PROVIDER = 'fast2sms'

# For Way2SMS
DEFAULT_SMS_PROVIDER = 'way2sms'

# For MSG91
DEFAULT_SMS_PROVIDER = 'msg91'
```

## 🐛 **Troubleshooting**

### Free Simulation Not Working?
- Check console output where you run `python manage.py runserver`
- Check `sms.log` file in project directory
- Ensure `DEFAULT_SMS_PROVIDER = 'free'` in settings.py

### Real SMS Not Received?
- Verify API credentials are correct
- Check account balance/credits
- Ensure mobile number format is correct (+919876543210)
- Check spam folder

### API Errors?
- Run test command: `python manage.py test_sms +919876543210`
- Check service status on provider website
- Verify account is active and verified

## 💡 **Pro Tips**

1. **Start with Free Simulation** - Test your app logic first
2. **Use Fast2SMS for real testing** - 100 free SMS is generous
3. **Keep console open** - You'll see OTP codes immediately
4. **Test with your own number** - Verify SMS delivery works
5. **Check logs** - All SMS attempts are logged for debugging

## 🎯 **Recommended Workflow**

1. **Development**: Use `free` provider (no setup, unlimited)
2. **Testing**: Use `fast2sms` (real SMS, 100 free)
3. **Production**: Use `msg91` or `twilio` (reliable, paid)

Your app is ready to test OTP functionality right now with zero setup! 🚀