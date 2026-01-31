from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.http import JsonResponse
from django.db import models
from .forms import CustomUserCreationForm, CustomAuthenticationForm, OTPVerificationForm, CustomUserUpdateForm, ChangePasswordForm
from .models import CustomUser, OTPVerification
from .sms_services import send_otp_sms
import random
import string
import logging

logger = logging.getLogger(__name__)


class CustomLoginView(LoginView):
    """
    Custom login view that redirects to OTP verification instead of direct login
    """
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
    
    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            # Don't log in yet, redirect to OTP verification
            # Generate and send OTP
            otp_code = ''.join(random.choices(string.digits, k=6))
            
            # Delete any existing OTP for this user
            OTPVerification.objects.filter(user=user, is_verified=False).delete()
            
            # Create new OTP
            otp_verification = OTPVerification.objects.create(
                user=user,
                otp_code=otp_code
            )
            
            # Send OTP via SMS
            sms_result = send_otp_sms(user.mobile_no, otp_code)
            
            if sms_result['success']:
                # Store user ID in session for OTP verification
                self.request.session['pending_user_id'] = user.id
                messages.success(
                    self.request, 
                    f'OTP sent to your mobile number ending with ***{user.mobile_no[-3:]} via {sms_result["provider"]}'
                )
                return redirect('otp_verification')
            else:
                messages.error(
                    self.request, 
                    f'Failed to send OTP: {sms_result["message"]}. Please try again.'
                )
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Invalid username or password')
            return self.form_invalid(form)


def register_view(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {user.emp_name}! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def dashboard_view(request):
    """
    Dashboard view after successful login
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'user': request.user,
        'total_users': CustomUser.objects.count(),
    }
    return render(request, 'users/dashboard.html', context)


def otp_verification_view(request):
    """
    OTP verification view
    """
    if 'pending_user_id' not in request.session:
        messages.error(request, 'No pending login found. Please login again.')
        return redirect('login')
    
    user_id = request.session['pending_user_id']
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'Invalid session. Please login again.')
        return redirect('login')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp_code']
            
            # Get the latest OTP for this user
            try:
                otp_verification = OTPVerification.objects.filter(
                    user=user, 
                    is_verified=False
                ).latest('created_at')
                
                if otp_verification.is_expired():
                    messages.error(request, 'OTP has expired. Please request a new one.')
                    return render(request, 'users/otp_verification.html', {
                        'form': form, 
                        'user': user,
                        'show_resend': True
                    })
                
                if otp_verification.otp_code == entered_otp:
                    # OTP is correct
                    otp_verification.is_verified = True
                    otp_verification.save()
                    
                    # Log in the user
                    login(request, user)
                    
                    # Clear the session
                    del request.session['pending_user_id']
                    
                    messages.success(request, f'Welcome back, {user.emp_name}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Invalid OTP. Please try again.')
                    
            except OTPVerification.DoesNotExist:
                messages.error(request, 'No valid OTP found. Please request a new one.')
                return render(request, 'users/otp_verification.html', {
                    'form': form, 
                    'user': user,
                    'show_resend': True
                })
    else:
        form = OTPVerificationForm()
    
    return render(request, 'users/otp_verification.html', {
        'form': form, 
        'user': user,
        'show_resend': False
    })


def resend_otp_view(request):
    """
    Resend OTP view
    """
    if 'pending_user_id' not in request.session:
        return JsonResponse({'success': False, 'message': 'No pending login found'})
    
    user_id = request.session['pending_user_id']
    try:
        user = CustomUser.objects.get(id=user_id)
        
        # Generate new OTP
        otp_code = ''.join(random.choices(string.digits, k=6))
        
        # Delete old OTPs
        OTPVerification.objects.filter(user=user, is_verified=False).delete()
        
        # Create new OTP
        OTPVerification.objects.create(
            user=user,
            otp_code=otp_code
        )
        
        # Send OTP via SMS
        sms_result = send_otp_sms(user.mobile_no, otp_code)
        
        if sms_result['success']:
            return JsonResponse({
                'success': True, 
                'message': f'New OTP sent to ***{user.mobile_no[-3:]} via {sms_result["provider"]}'
            })
        else:
            return JsonResponse({
                'success': False, 
                'message': f'Failed to send OTP: {sms_result["message"]}'
            })
        
    except CustomUser.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid session'})

def test_otp_view(request):
    """
    Test OTP interface for developers
    """
    return render(request, 'users/test_otp.html')


def test_otp_api(request):
    """
    API endpoint to test SMS sending
    """
    if request.method == 'POST':
        mobile_number = request.POST.get('mobile_number')
        provider = request.POST.get('provider', 'free')
        
        if not mobile_number:
            return JsonResponse({
                'success': False,
                'message': 'Mobile number is required',
                'provider': provider
            })
        
        # Generate test OTP
        test_otp = ''.join(random.choices(string.digits, k=6))
        
        # Send SMS
        result = send_otp_sms(mobile_number, test_otp, provider)
        
        # Add OTP code to response for testing
        result['otp_code'] = test_otp
        
        return JsonResponse(result)
    
    return JsonResponse({
        'success': False,
        'message': 'Only POST method allowed'
    })

def user_list_view(request):
    """
    Display all users in a table format with view, update, delete options
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Check if user has permission to view user list
    allowed_roles = ['commissioner', 'zone_commissioner', 'ulb_admin', 'assistant_project_manager', 'circle_manager']
    if request.user.role not in allowed_roles and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view the user list.')
        return redirect('dashboard')
    
    # Get all users with search and filter functionality
    users = CustomUser.objects.all().order_by('emp_code')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            models.Q(emp_name__icontains=search_query) |
            models.Q(emp_code__icontains=search_query) |
            models.Q(username__icontains=search_query) |
            models.Q(email__icontains=search_query) |
            models.Q(mobile_no__icontains=search_query)
        )
    
    # Role filter
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Status filter
    status_filter = request.GET.get('status', '')
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'status_filter': status_filter,
        'role_choices': CustomUser.ROLE_CHOICES,
        'total_users': users.count(),
    }
    
    return render(request, 'users/user_list.html', context)


def user_detail_view(request, user_id):
    """
    View detailed information of a specific user
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user_list')
    
    # Check permissions
    allowed_roles = ['commissioner', 'zone_commissioner', 'ulb_admin', 'assistant_project_manager', 'circle_manager']
    if request.user.role not in allowed_roles and not request.user.is_staff and request.user != user:
        messages.error(request, 'You do not have permission to view this user.')
        return redirect('dashboard')
    
    context = {
        'user_detail': user,
    }
    
    return render(request, 'users/user_detail.html', context)


def user_update_view(request, user_id):
    """
    Update user information
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user_to_update = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user_list')
    
    # Check permissions
    allowed_roles = ['commissioner', 'zone_commissioner', 'ulb_admin', 'assistant_project_manager', 'circle_manager']
    if request.user.role not in allowed_roles and not request.user.is_staff:
        messages.error(request, 'You do not have permission to update users.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user_to_update)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user_to_update.emp_name} updated successfully!')
            return redirect('user_detail', user_id=user_to_update.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserUpdateForm(instance=user_to_update)
    
    context = {
        'form': form,
        'user_to_update': user_to_update,
        'is_update': True,
    }
    
    return render(request, 'users/user_update.html', context)


def user_delete_view(request, user_id):
    """
    Delete user (with confirmation)
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    try:
        user_to_delete = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('user_list')
    
    # Check permissions - only high-level roles can delete users
    allowed_roles = ['commissioner', 'zone_commissioner', 'ulb_admin']
    if request.user.role not in allowed_roles and not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete users.')
        return redirect('dashboard')
    
    # Prevent self-deletion
    if request.user == user_to_delete:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('user_list')
    
    if request.method == 'POST':
        user_name = user_to_delete.emp_name
        user_to_delete.delete()
        messages.success(request, f'User {user_name} deleted successfully!')
        return redirect('user_list')
    
    context = {
        'user_to_delete': user_to_delete,
    }
    
    return render(request, 'users/user_delete.html', context)
def change_password_view(request):
    """
    Allow users to change their password after login
    """
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            
            # Update session to prevent logout after password change
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, request.user)
            
            messages.success(
                request, 
                'Your password has been changed successfully! You can now use your new password for future logins.'
            )
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ChangePasswordForm(request.user)
    
    context = {
        'form': form,
    }
    
    return render(request, 'users/change_password.html', context)