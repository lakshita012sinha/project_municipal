from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification


class CustomUserAdmin(UserAdmin):
    """
    Custom User Admin with additional fields
    """
    model = CustomUser
    list_display = ['username', 'emp_name', 'emp_code', 'email', 'get_role_display', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'emp_name', 'emp_code', 'email']
    ordering = ['emp_code']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Employee Information', {
            'fields': ('emp_name', 'emp_code', 'mobile_no', 'report_to', 'image', 'role')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Employee Information', {
            'fields': ('emp_name', 'emp_code', 'mobile_no', 'email', 'report_to', 'image', 'role')
        }),
    )
    
    def get_role_display(self, obj):
        return obj.get_role_display()
    get_role_display.short_description = 'Role'


class OTPVerificationAdmin(admin.ModelAdmin):
    """
    Admin for OTP Verification
    """
    list_display = ['user', 'otp_code', 'created_at', 'expires_at', 'is_verified']
    list_filter = ['is_verified', 'created_at']
    search_fields = ['user__username', 'user__emp_name', 'otp_code']
    readonly_fields = ['created_at', 'expires_at']
    ordering = ['-created_at']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTPVerification, OTPVerificationAdmin)