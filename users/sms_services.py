"""
SMS Service Integration for OTP Delivery
Supports multiple SMS providers: Twilio, MSG91, and TextLocal
"""

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class SMSServiceError(Exception):
    """Custom exception for SMS service errors"""
    pass


class BaseSMSService:
    """Base class for SMS services"""
    
    def send_otp(self, mobile_number, otp_code, template_message=None):
        """
        Send OTP to mobile number
        Args:
            mobile_number: Phone number with country code
            otp_code: 6-digit OTP code
            template_message: Custom message template
        Returns:
            dict: Response with success status and message
        """
        raise NotImplementedError("Subclasses must implement send_otp method")
    
    def format_mobile_number(self, mobile_number):
        """Format mobile number with country code"""
        # Remove any spaces, dashes, or special characters
        mobile_number = ''.join(filter(str.isdigit, mobile_number))
        
        # Add +91 for Indian numbers if not present
        if len(mobile_number) == 10:
            mobile_number = f"+91{mobile_number}"
        elif len(mobile_number) == 12 and mobile_number.startswith("91"):
            mobile_number = f"+{mobile_number}"
        elif not mobile_number.startswith("+"):
            mobile_number = f"+{mobile_number}"
            
        return mobile_number


class TwilioSMSService(BaseSMSService):
    """Twilio SMS Service Implementation"""
    
    def __init__(self):
        self.account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        self.auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        self.from_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        
        # Check if credentials are properly configured (not placeholders)
        if (not all([self.account_sid, self.auth_token, self.from_number]) or
            self.account_sid == 'your_twilio_account_sid_here' or
            self.auth_token == 'your_twilio_auth_token_here' or
            self.from_number == '+1234567890'):
            raise ImproperlyConfigured(
                "Twilio credentials not properly configured. "
                "Please sign up at https://www.twilio.com/ and set TWILIO_ACCOUNT_SID, "
                "TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in settings. "
                "Current values are placeholders or empty."
            )
    
    def send_otp(self, mobile_number, otp_code, template_message=None):
        try:
            from twilio.rest import Client
            
            client = Client(self.account_sid, self.auth_token)
            mobile_number = self.format_mobile_number(mobile_number)
            
            message_body = template_message or f"Your OTP for Rajasthan Municipal login is: {otp_code}. Valid for 5 minutes. Do not share this code."
            
            message = client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=mobile_number
            )
            
            logger.info(f"Twilio SMS sent successfully. SID: {message.sid}")
            return {
                'success': True,
                'message': 'OTP sent successfully',
                'provider': 'Twilio',
                'message_id': message.sid
            }
            
        except ImportError:
            raise SMSServiceError("Twilio library not installed. Run: pip install twilio")
        except Exception as e:
            logger.error(f"Twilio SMS failed: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'Twilio'
            }


class MSG91SMSService(BaseSMSService):
    """MSG91 SMS Service Implementation (India-focused)"""
    
    def __init__(self):
        self.auth_key = getattr(settings, 'MSG91_AUTH_KEY', None)
        self.sender_id = getattr(settings, 'MSG91_SENDER_ID', 'OTPSMS')
        self.route = getattr(settings, 'MSG91_ROUTE', '4')  # 4 for transactional
        
        # Check if auth key is properly configured (not placeholder)
        if not self.auth_key or self.auth_key == 'your_msg91_auth_key_here':
            raise ImproperlyConfigured(
                "MSG91 Auth Key not properly configured. "
                "Please sign up at https://msg91.com/ and set MSG91_AUTH_KEY in settings. "
                "Current value is placeholder or empty."
            )
    
    def send_otp(self, mobile_number, otp_code, template_message=None):
        try:
            mobile_number = self.format_mobile_number(mobile_number).replace('+91', '')
            
            message_body = template_message or f"Your OTP for Rajasthan Municipal login is {otp_code}. Valid for 5 minutes. Do not share this code."
            
            url = "https://api.msg91.com/api/sendhttp.php"
            
            payload = {
                'authkey': self.auth_key,
                'mobiles': mobile_number,
                'message': message_body,
                'sender': self.sender_id,
                'route': self.route,
                'country': '91'
            }
            
            response = requests.get(url, params=payload, timeout=30)
            
            if response.status_code == 200:
                response_text = response.text.strip()
                if response_text.startswith('5'):  # MSG91 success response starts with 5
                    logger.info(f"MSG91 SMS sent successfully. Response: {response_text}")
                    return {
                        'success': True,
                        'message': 'OTP sent successfully',
                        'provider': 'MSG91',
                        'message_id': response_text
                    }
                else:
                    logger.error(f"MSG91 SMS failed. Response: {response_text}")
                    return {
                        'success': False,
                        'message': f'MSG91 Error: {response_text}',
                        'provider': 'MSG91'
                    }
            else:
                logger.error(f"MSG91 HTTP Error: {response.status_code}")
                return {
                    'success': False,
                    'message': f'HTTP Error: {response.status_code}',
                    'provider': 'MSG91'
                }
                
        except requests.RequestException as e:
            logger.error(f"MSG91 Request failed: {str(e)}")
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'provider': 'MSG91'
            }
        except Exception as e:
            logger.error(f"MSG91 SMS failed: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'MSG91'
            }


class TextLocalSMSService(BaseSMSService):
    """TextLocal SMS Service Implementation (India)"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'TEXTLOCAL_API_KEY', None)
        self.sender = getattr(settings, 'TEXTLOCAL_SENDER', 'TXTLCL')
        
        # Check if API key is properly configured (not placeholder)
        if not self.api_key or self.api_key == 'your_textlocal_api_key_here':
            raise ImproperlyConfigured(
                "TextLocal API key not properly configured. "
                "Please sign up at https://www.textlocal.in/ and set TEXTLOCAL_API_KEY in settings. "
                "Current value is placeholder or empty."
            )
    
    def send_otp(self, mobile_number, otp_code, template_message=None):
        try:
            mobile_number = self.format_mobile_number(mobile_number).replace('+91', '')
            
            message_body = template_message or f"Your OTP for Rajasthan Municipal login is {otp_code}. Valid for 5 minutes."
            
            url = "https://api.textlocal.in/send/"
            
            data = {
                'apikey': self.api_key,
                'numbers': mobile_number,
                'message': message_body,
                'sender': self.sender
            }
            
            response = requests.post(url, data=data, timeout=30)
            response_data = response.json()
            
            if response_data.get('status') == 'success':
                logger.info(f"TextLocal SMS sent successfully. Response: {response_data}")
                return {
                    'success': True,
                    'message': 'OTP sent successfully',
                    'provider': 'TextLocal',
                    'message_id': response_data.get('messages', [{}])[0].get('id')
                }
            else:
                error_msg = response_data.get('errors', [{}])[0].get('message', 'Unknown error')
                logger.error(f"TextLocal SMS failed: {error_msg}")
                return {
                    'success': False,
                    'message': f'TextLocal Error: {error_msg}',
                    'provider': 'TextLocal'
                }
                
        except requests.RequestException as e:
            logger.error(f"TextLocal Request failed: {str(e)}")
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'provider': 'TextLocal'
            }
        except Exception as e:
            logger.error(f"TextLocal SMS failed: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'TextLocal'
            }


class Fast2SMSService(BaseSMSService):
    """Fast2SMS Service Implementation (India) - Free tier available"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'FAST2SMS_API_KEY', None)
        self.sender_id = getattr(settings, 'FAST2SMS_SENDER_ID', 'FSTSMS')
        
        # Check if API key is properly configured (not placeholder)
        if not self.api_key or self.api_key == 'your_fast2sms_api_key_here':
            raise ImproperlyConfigured(
                "Fast2SMS API key not properly configured. "
                "Please sign up at https://www.fast2sms.com/ and set FAST2SMS_API_KEY in settings. "
                "Current value is placeholder or empty."
            )
    
    def send_otp(self, mobile_number, otp_code, template_message=None):
        try:
            mobile_number = self.format_mobile_number(mobile_number).replace('+91', '')
            
            message_body = template_message or f"Your OTP for Rajasthan Municipal login is {otp_code}. Valid for 5 minutes. Do not share."
            
            url = "https://www.fast2sms.com/dev/bulkV2"
            
            payload = {
                'authorization': self.api_key,
                'sender_id': self.sender_id,
                'message': message_body,
                'language': 'english',
                'route': 'q',  # Quick route
                'numbers': mobile_number,
            }
            
            headers = {
                'cache-control': "no-cache"
            }
            
            response = requests.post(url, data=payload, headers=headers, timeout=30)
            
            # Handle different response formats
            try:
                response_data = response.json()
            except ValueError:
                # If response is not JSON, treat as error
                logger.error(f"Fast2SMS non-JSON response: {response.text}")
                return {
                    'success': False,
                    'message': f'Invalid response format: {response.text[:100]}',
                    'provider': 'Fast2SMS'
                }
            
            if response_data.get('return') == True:
                logger.info(f"Fast2SMS sent successfully. Response: {response_data}")
                return {
                    'success': True,
                    'message': 'OTP sent successfully',
                    'provider': 'Fast2SMS',
                    'message_id': response_data.get('request_id')
                }
            else:
                error_msg = response_data.get('message', 'Unknown error')
                logger.error(f"Fast2SMS failed: {error_msg}")
                
                # Check for authentication errors
                if 'authentication' in error_msg.lower() or 'authorization' in error_msg.lower():
                    error_msg += " - Please check your API key at https://www.fast2sms.com/"
                
                return {
                    'success': False,
                    'message': f'Fast2SMS Error: {error_msg}',
                    'provider': 'Fast2SMS'
                }
                
        except requests.RequestException as e:
            logger.error(f"Fast2SMS Request failed: {str(e)}")
            return {
                'success': False,
                'message': f'Network error: {str(e)}',
                'provider': 'Fast2SMS'
            }
        except Exception as e:
            logger.error(f"Fast2SMS failed: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'Fast2SMS'
            }


class Way2SMSService(BaseSMSService):
    """Way2SMS Service Implementation (India) - Free service"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'WAY2SMS_API_KEY', None)
        
        if not self.api_key:
            raise ImproperlyConfigured(
                "Way2SMS credentials not properly configured. "
                "Please set WAY2SMS_API_KEY in settings."
            )
    
    def send_otp(self, mobile_number, otp_code, template_message=None):
        try:
            mobile_number = self.format_mobile_number(mobile_number).replace('+91', '')
            
            message_body = template_message or f"Your OTP: {otp_code}. Valid for 5 minutes."
            
            url = "https://www.way2sms.com/api/v1/sendCampaign"
            
            payload = {
                'apikey': self.api_key,
                'secret': getattr(settings, 'WAY2SMS_SECRET', ''),
                'usetype': 'stage',  # Use 'prod' for production
                'phone': mobile_number,
                'message': message_body,
                'senderid': 'Way2SMS'
            }
            
            response = requests.post(url, data=payload, timeout=30)
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('status') == 'success':
                    logger.info(f"Way2SMS sent successfully")
                    return {
                        'success': True,
                        'message': 'OTP sent successfully',
                        'provider': 'Way2SMS',
                        'message_id': response_data.get('campaignId')
                    }
                else:
                    error_msg = response_data.get('message', 'Unknown error')
                    return {
                        'success': False,
                        'message': f'Way2SMS Error: {error_msg}',
                        'provider': 'Way2SMS'
                    }
            else:
                return {
                    'success': False,
                    'message': f'HTTP Error: {response.status_code}',
                    'provider': 'Way2SMS'
                }
                
        except Exception as e:
            logger.error(f"Way2SMS failed: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'Way2SMS'
            }


class FreeSMSService(BaseSMSService):
    """Free SMS Service for Testing - Simulates SMS with detailed logging"""
    
    def __init__(self):
        self.test_mode = getattr(settings, 'SMS_TEST_MODE', True)
        self.allowed_numbers = getattr(settings, 'SMS_TEST_NUMBERS', [])
    
    def send_otp(self, mobile_number, otp_code, template_message=None):
        try:
            mobile_number = self.format_mobile_number(mobile_number)
            message_body = template_message or f"Your OTP for Rajasthan Municipal login is {otp_code}. Valid for 5 minutes."
            
            # Log the SMS details
            logger.info("="*60)
            logger.info("FREE SMS SERVICE - OTP SENT")
            logger.info("="*60)
            logger.info(f"Mobile Number: {mobile_number}")
            logger.info(f"OTP Code: {otp_code}")
            logger.info(f"Message: {message_body}")
            logger.info(f"Timestamp: {timezone.now()}")
            logger.info("="*60)
            
            # Also print to console for immediate visibility
            print("\n" + "="*60)
            print("FREE SMS SERVICE - OTP SENT")
            print("="*60)
            print(f"Mobile Number: {mobile_number}")
            print(f"OTP Code: {otp_code}")
            print(f"Message: {message_body}")
            print(f"Timestamp: {timezone.now()}")
            print("="*60 + "\n")
            
            # Check if number is in allowed test numbers
            if self.allowed_numbers and mobile_number not in self.allowed_numbers:
                return {
                    'success': False,
                    'message': f'Number {mobile_number} not in test allowed list',
                    'provider': 'FreeSMS'
                }
            
            return {
                'success': True,
                'message': 'OTP sent successfully (simulated)',
                'provider': 'FreeSMS',
                'message_id': f'free_sms_{timezone.now().timestamp()}'
            }
            
        except Exception as e:
            logger.error(f"FreeSMS failed: {str(e)}")
            return {
                'success': False,
                'message': f'Failed to send SMS: {str(e)}',
                'provider': 'FreeSMS'
            }


class SMSServiceFactory:
    """Factory class to get the appropriate SMS service"""
    
    SERVICES = {
        'twilio': TwilioSMSService,
        'msg91': MSG91SMSService,
        'textlocal': TextLocalSMSService,
        'fast2sms': Fast2SMSService,
        'way2sms': Way2SMSService,
        'free': FreeSMSService,
    }
    
    @classmethod
    def get_service(cls, provider=None):
        """
        Get SMS service instance
        Args:
            provider: SMS provider name ('twilio', 'msg91', 'textlocal')
        Returns:
            SMS service instance
        """
        if provider is None:
            provider = getattr(settings, 'DEFAULT_SMS_PROVIDER', 'free')
        
        provider = provider.lower()
        
        if provider not in cls.SERVICES:
            raise ValueError(f"Unsupported SMS provider: {provider}")
        
        try:
            return cls.SERVICES[provider]()
        except ImproperlyConfigured as e:
            logger.warning(f"SMS service configuration error for {provider}: {e}")
            # Try fallback providers (free service as ultimate fallback)
            fallback_order = ['free', 'fast2sms', 'msg91', 'textlocal', 'twilio']
            for fallback_provider in fallback_order:
                if fallback_provider != provider:
                    try:
                        logger.info(f"Trying fallback SMS provider: {fallback_provider}")
                        return cls.SERVICES[fallback_provider]()
                    except ImproperlyConfigured:
                        continue
            
            # If all configured services fail, return free service
            logger.warning("All configured SMS services failed, using free simulation service")
            return cls.SERVICES['free']()


def send_otp_sms(mobile_number, otp_code, provider=None):
    """
    Convenience function to send OTP SMS
    Args:
        mobile_number: Phone number
        otp_code: OTP code
        provider: SMS provider ('twilio', 'msg91', 'textlocal')
    Returns:
        dict: Response with success status and message
    """
    try:
        sms_service = SMSServiceFactory.get_service(provider)
        return sms_service.send_otp(mobile_number, otp_code)
    except Exception as e:
        logger.error(f"SMS sending failed: {str(e)}")
        return {
            'success': False,
            'message': f'SMS service error: {str(e)}',
            'provider': provider or 'unknown'
        }