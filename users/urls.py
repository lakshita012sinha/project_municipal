from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('otp-verification/', views.otp_verification_view, name='otp_verification'),
    path('resend-otp/', views.resend_otp_view, name='resend_otp'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('test-otp/', views.test_otp_view, name='test_otp'),
    path('api/test-otp/', views.test_otp_api, name='test_otp_api'),
    
    # User Management URLs
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('users/<int:user_id>/update/', views.user_update_view, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete_view, name='user_delete'),
    
    # Password Management
    path('change-password/', views.change_password_view, name='change_password'),
    
    path('', views.dashboard_view, name='home'),
]