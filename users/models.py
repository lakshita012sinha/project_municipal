from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import random
import string


class CustomUser(AbstractUser):
    
    emp_name = models.CharField(max_length=100, verbose_name="Employee Name")
    emp_code = models.CharField(max_length=20, unique=True, verbose_name="Employee Code")
    mobile_no = models.CharField(max_length=15, verbose_name="Mobile Number")
    report_to = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Reports To"
    )
    image = models.ImageField(upload_to='user_images/', blank=True, null=True, verbose_name="Profile Image")
    
    ROLE_CHOICES = [
        ('assistant_project_manager', 'Assistant Project Manager'),
        ('circle_manager', 'Circle Manager'),
        ('team_leader', 'Team Leader'),
        ('back_office_head', 'Back Office Head'),
        ('back_office', 'Back Office'),
        ('accountant', 'Accountant'),
        ('flying_officer_sspl', 'Flying Officer SSPL'),
        ('revenue_officer', 'Revenue Officer'),
        ('zone_commissioner', 'Zone Commissioner'),
        ('revenue_inspector', 'Revenue Inspector'),
        ('surveyor', 'Surveyor'),
        ('tax_collector', 'Tax Collector'),
        ('tele_caller', 'Tele Caller'),
        ('mis', 'MIS'),
        ('counter', 'Counter'),
        ('commissioner', 'Commissioner'),
        ('oswal', 'Oswal'),
        ('ulb_admin', 'ULB Admin'),
        ('qr_installer', 'QR Installer'),
        ('dc_revenue_first', 'DC Revenue First'),
        ('ro_revenue_first', 'RO Revenue First'),
        ('testt', 'TESTT'),
    ]
    
    role = models.CharField(
        max_length=30, 
        choices=ROLE_CHOICES, 
        default='back_office',
        verbose_name="Role"
    )
    
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(unique=True, blank=False)
    
    def __str__(self):
        return f"{self.emp_name} ({self.emp_code})"
    
    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class OTPVerification(models.Model):
    """
    Model to store OTP verification details
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        if not self.expires_at:
            # OTP expires in 5 minutes
            self.expires_at = timezone.now() + timezone.timedelta(minutes=5)
        super().save(*args, **kwargs)
    
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def __str__(self):
        return f"OTP for {self.user.username} - {self.otp_code}"
    
    class Meta:
        ordering = ['-created_at']