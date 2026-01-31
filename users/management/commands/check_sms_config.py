from django.core.management.base import BaseCommand
from django.conf import settings
from users.sms_services import SMSServiceFactory


class Command(BaseCommand):
    help = 'Check SMS service configuration and provide setup guidance'

    def handle(self, *args, **options):
        self.stdout.write("🔍 Checking SMS Configuration...")
        self.stdout.write("=" * 60)
        
        # Check current default provider
        default_provider = getattr(settings, 'DEFAULT_SMS_PROVIDER', 'free')
        self.stdout.write(f"📋 Default SMS Provider: {default_provider}")
        
        # Check each service configuration
        services_status = {
            'free': self.check_free_service(),
            'fast2sms': self.check_fast2sms(),
            'msg91': self.check_msg91(),
            'twilio': self.check_twilio(),
            'textlocal': self.check_textlocal(),
            'way2sms': self.check_way2sms(),
        }
        
        self.stdout.write("\n📊 Service Configuration Status:")
        self.stdout.write("-" * 40)
        
        configured_count = 0
        for service, status in services_status.items():
            if status['configured']:
                configured_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {service.upper()}: {status['message']}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  {service.upper()}: {status['message']}")
                )
        
        # Provide recommendations
        self.stdout.write(f"\n📈 Summary: {configured_count}/6 services configured")
        
        if configured_count == 0:
            self.stdout.write(
                self.style.ERROR("❌ No SMS services configured!")
            )
        elif services_status['free']['configured']:
            self.stdout.write(
                self.style.SUCCESS("✅ Free simulation service is available for testing")
            )
        
        # Provide setup recommendations
        self.stdout.write("\n💡 Recommendations:")
        self.stdout.write("-" * 20)
        
        if not services_status['free']['configured']:
            self.stdout.write("1. Free service should always work - check configuration")
        
        if not services_status['fast2sms']['configured']:
            self.stdout.write("2. For real SMS testing: Set up Fast2SMS (100 free SMS)")
            self.stdout.write("   - Sign up: https://www.fast2sms.com/")
            self.stdout.write("   - Get API key from Dashboard")
            self.stdout.write("   - Set FAST2SMS_API_KEY in settings.py")
        
        if not services_status['msg91']['configured']:
            self.stdout.write("3. For production: Set up MSG91 (reliable, cost-effective)")
            self.stdout.write("   - Sign up: https://msg91.com/")
            self.stdout.write("   - Get Auth Key from API section")
            self.stdout.write("   - Set MSG91_AUTH_KEY in settings.py")
        
        # Test current default provider
        self.stdout.write(f"\n🧪 Testing default provider ({default_provider}):")
        try:
            service = SMSServiceFactory.get_service(default_provider)
            self.stdout.write(
                self.style.SUCCESS(f"✅ {default_provider} service initialized successfully")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ {default_provider} service failed: {str(e)}")
            )
            self.stdout.write("💡 Falling back to free service for now")
    
    def check_free_service(self):
        """Check free simulation service"""
        try:
            from users.sms_services import FreeSMSService
            service = FreeSMSService()
            return {
                'configured': True,
                'message': 'Ready (no setup needed)'
            }
        except Exception as e:
            return {
                'configured': False,
                'message': f'Error: {str(e)}'
            }
    
    def check_fast2sms(self):
        """Check Fast2SMS configuration"""
        api_key = getattr(settings, 'FAST2SMS_API_KEY', None)
        
        if not api_key or api_key == 'your_fast2sms_api_key_here':
            return {
                'configured': False,
                'message': 'API key not set (sign up at fast2sms.com)'
            }
        
        return {
            'configured': True,
            'message': f'API key configured (ends with ...{api_key[-4:]})'
        }
    
    def check_msg91(self):
        """Check MSG91 configuration"""
        auth_key = getattr(settings, 'MSG91_AUTH_KEY', None)
        
        if not auth_key or auth_key == 'your_msg91_auth_key_here':
            return {
                'configured': False,
                'message': 'Auth key not set (sign up at msg91.com)'
            }
        
        return {
            'configured': True,
            'message': f'Auth key configured (ends with ...{auth_key[-4:]})'
        }
    
    def check_twilio(self):
        """Check Twilio configuration"""
        account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        phone_number = getattr(settings, 'TWILIO_PHONE_NUMBER', None)
        
        if (not all([account_sid, auth_token, phone_number]) or
            account_sid == 'your_twilio_account_sid_here' or
            auth_token == 'your_twilio_auth_token_here' or
            phone_number == '+1234567890'):
            return {
                'configured': False,
                'message': 'Credentials not set (sign up at twilio.com)'
            }
        
        return {
            'configured': True,
            'message': f'Configured with number {phone_number}'
        }
    
    def check_textlocal(self):
        """Check TextLocal configuration"""
        api_key = getattr(settings, 'TEXTLOCAL_API_KEY', None)
        
        if not api_key or api_key == 'your_textlocal_api_key_here':
            return {
                'configured': False,
                'message': 'API key not set (sign up at textlocal.in)'
            }
        
        return {
            'configured': True,
            'message': f'API key configured (ends with ...{api_key[-4:]})'
        }
    
    def check_way2sms(self):
        """Check Way2SMS configuration"""
        api_key = getattr(settings, 'WAY2SMS_API_KEY', None)
        secret = getattr(settings, 'WAY2SMS_SECRET', None)
        
        if (not api_key or not secret or 
            api_key == 'your_way2sms_api_key_here' or
            secret == 'your_way2sms_secret_here'):
            return {
                'configured': False,
                'message': 'Credentials not set (sign up at way2sms.com)'
            }
        
        return {
            'configured': True,
            'message': 'API key and secret configured'
        }