from django.core.management.base import BaseCommand
from users.sms_services import send_otp_sms, SMSServiceFactory


class Command(BaseCommand):
    help = 'Test SMS service configuration'

    def add_arguments(self, parser):
        parser.add_argument(
            'mobile_number',
            type=str,
            help='Mobile number to send test SMS (with country code, e.g., +919876543210)'
        )
        parser.add_argument(
            '--provider',
            type=str,
            choices=['free', 'fast2sms', 'way2sms', 'msg91', 'twilio', 'textlocal'],
            help='SMS provider to test (default: from settings)'
        )

    def handle(self, *args, **options):
        mobile_number = options['mobile_number']
        provider = options.get('provider')
        
        self.stdout.write(f"Testing SMS service...")
        self.stdout.write(f"Mobile Number: {mobile_number}")
        self.stdout.write(f"Provider: {provider or 'default from settings'}")
        
        try:
            # Test OTP sending
            test_otp = '123456'
            result = send_otp_sms(mobile_number, test_otp, provider)
            
            if result['success']:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ SMS sent successfully via {result['provider']}!"
                    )
                )
                self.stdout.write(f"Message ID: {result.get('message_id', 'N/A')}")
                self.stdout.write(f"Check your mobile for OTP: {test_otp}")
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ SMS sending failed: {result['message']}"
                    )
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Error: {str(e)}")
            )
            
        # Test service configuration
        self.stdout.write("\n" + "="*50)
        self.stdout.write("Testing service configurations:")
        
        for service_name in ['free', 'fast2sms', 'way2sms', 'msg91', 'twilio', 'textlocal']:
            try:
                service = SMSServiceFactory.get_service(service_name)
                self.stdout.write(
                    self.style.SUCCESS(f"✅ {service_name.upper()}: Configured")
                )
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  {service_name.upper()}: {str(e)}")
                )