from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, OTPVerification


class CustomUserCreationForm(UserCreationForm):
    """
    Custom user registration form with additional fields
    """
    emp_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Name'})
    )
    emp_code = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Employee Code'})
    )
    mobile_no = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'})
    )
    report_to = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Select Reporting Manager"
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=CustomUser.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'emp_name', 'emp_code', 'mobile_no', 'email', 
                 'report_to', 'image', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to default fields
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom login form with styling
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })


class OTPVerificationForm(forms.Form):
    """
    Form for OTP verification
    """
    otp_code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control text-center',
            'placeholder': 'Enter 6-digit OTP',
            'style': 'font-size: 1.5rem; letter-spacing: 0.5rem;'
        }),
        help_text="Enter the 6-digit OTP sent to your mobile number"
    )
    
    def clean_otp_code(self):
        otp_code = self.cleaned_data.get('otp_code')
        if not otp_code.isdigit():
            raise forms.ValidationError("OTP must contain only digits")
        return otp_code

class CustomUserUpdateForm(forms.ModelForm):
    """
    Custom user update form that handles password updates properly
    """
    password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Leave empty to keep current password'}),
        required=False,
        help_text="Leave empty to keep current password"
    )
    password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new password'}),
        required=False,
        help_text="Enter the same password as before, for verification"
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'emp_name', 'emp_code', 'mobile_no', 'email', 
                 'report_to', 'image', 'role', 'is_active', 'is_staff', 'is_superuser')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_name': forms.TextInput(attrs={'class': 'form-control'}),
            'emp_code': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_no': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'report_to': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude the current user from report_to choices to prevent circular reporting
        if self.instance and self.instance.pk:
            self.fields['report_to'].queryset = CustomUser.objects.exclude(pk=self.instance.pk)
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 or password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        return user

class ChangePasswordForm(forms.Form):
    """
    Form for users to change their password after login
    """
    current_password = forms.CharField(
        label="Current Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your current password'
        }),
        help_text="Enter your current password for verification"
    )
    
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new password'
        }),
        help_text="Your password must contain at least 8 characters"
    )
    
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm new password'
        }),
        help_text="Enter the same password as before, for verification"
    )
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean_current_password(self):
        """
        Validate that the current password is correct
        """
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("Your current password is incorrect.")
        return current_password
    
    def clean_new_password2(self):
        """
        Validate that the two password entries match
        """
        new_password1 = self.cleaned_data.get('new_password1')
        new_password2 = self.cleaned_data.get('new_password2')
        
        if new_password1 and new_password2:
            if new_password1 != new_password2:
                raise forms.ValidationError("The two password fields didn't match.")
        return new_password2
    
    def clean_new_password1(self):
        """
        Validate the new password strength
        """
        new_password1 = self.cleaned_data.get('new_password1')
        
        if new_password1:
            # Check minimum length
            if len(new_password1) < 8:
                raise forms.ValidationError("Password must be at least 8 characters long.")
            
            # Check if password is too common
            common_passwords = ['password', '12345678', 'qwerty', 'abc123', 'password123']
            if new_password1.lower() in common_passwords:
                raise forms.ValidationError("This password is too common. Please choose a more secure password.")
            
            # Check if password is same as current
            if self.user.check_password(new_password1):
                raise forms.ValidationError("New password cannot be the same as your current password.")
        
        return new_password1
    
    def save(self):
        """
        Save the new password
        """
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        self.user.save()
        return self.user