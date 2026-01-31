# Django User Management System Setup Instructions

## Overview
This Django application provides a complete user management system with OTP verification for the Rajasthan Municipal project.

## Features
- Custom user model with employee details (emp_name, emp_code, mobile_no, email, role, etc.)
- User registration with all required fields
- Login with username/password followed by OTP verification
- OTP sent to registered mobile number (simulated in console for development)
- Dashboard with user profile and basic statistics
- Admin panel for user management

## Setup Instructions

### 1. Install Required Packages
```bash
pip install Django Pillow
```

### 2. Run Database Migrations
```bash
cd Rajasthan_Municipal
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser
```bash
python manage.py createsuperuser
```
When prompted, provide the additional fields:
- Employee Name
- Employee Code
- Mobile Number
- Role (choose 'admin')

### 4. Run Development Server
```bash
python manage.py runserver
```

### 5. Access the Application
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/
- Login page: http://127.0.0.1:8000/login/
- Registration: http://127.0.0.1:8000/register/

## User Flow

### Registration Process
1. Admin or authorized user goes to `/register/`
2. Fills out the complete form with:
   - Employee Name
   - Employee Code (unique)
   - Mobile Number
   - Email Address
   - Username
   - Password
   - Reports To (optional)
   - Profile Image (optional)
   - Role
3. Account is created and user can login

### Login Process
1. User goes to `/login/`
2. Enters username and password
3. If credentials are correct, OTP is generated and sent to registered mobile
4. User is redirected to OTP verification page
5. User enters 6-digit OTP
6. If OTP is correct, user is logged in and redirected to dashboard

## OTP System
- OTP is 6 digits long
- Expires in 5 minutes
- Can be resent with 60-second cooldown
- Currently simulated (printed to console)
- Ready for SMS service integration (Twilio, AWS SNS, etc.)

## File Structure
```
users/
├── models.py          # CustomUser and OTPVerification models
├── forms.py           # Registration, login, and OTP forms
├── views.py           # Login, registration, OTP verification views
├── admin.py           # Admin configuration
├── urls.py            # URL patterns
└── templates/users/   # HTML templates
    ├── base.html
    ├── login.html
    ├── register.html
    ├── otp_verification.html
    └── dashboard.html
```

## Customization Notes
- To integrate real SMS service, modify the `send_otp_sms()` function in views.py
- User roles can be extended in the ROLE_CHOICES in models.py
- Additional user fields can be added to the CustomUser model
- OTP expiry time can be modified in the OTPVerification model

## Security Features
- Password validation
- CSRF protection
- Session-based OTP verification
- OTP expiry mechanism
- Unique employee codes
- Role-based access (ready for extension)