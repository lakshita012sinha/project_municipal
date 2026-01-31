#!/usr/bin/env python
"""
Quick test script to verify role choices are working
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Rajasthan_Municipal.settings')
django.setup()

from users.models import CustomUser

def test_roles():
    print("Testing Role Choices...")
    print("=" * 50)
    
    # Display all available roles
    print("Available Roles:")
    for role_code, role_name in CustomUser.ROLE_CHOICES:
        print(f"  {role_code}: {role_name}")
    
    print(f"\nTotal roles available: {len(CustomUser.ROLE_CHOICES)}")
    
    # Test role validation
    print("\nTesting role validation...")
    valid_roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
    
    test_roles = ['commissioner', 'back_office', 'invalid_role']
    for role in test_roles:
        if role in valid_roles:
            print(f"✓ '{role}' is a valid role")
        else:
            print(f"✗ '{role}' is NOT a valid role")

if __name__ == "__main__":
    test_roles()