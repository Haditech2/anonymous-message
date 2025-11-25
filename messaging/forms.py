from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile, Message
import re


class CreateProfileForm(forms.Form):
    """Form for creating a new user profile"""
    username = forms.CharField(
        max_length=50,
        min_length=3,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Choose your username',
            'autocomplete': 'off'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower().strip()
        
        # Validate username format (alphanumeric and underscores only)
        if not re.match(r'^[a-z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, numbers, and underscores.')
        
        # Check if username already exists
        if UserProfile.objects.filter(username=username).exists():
            raise ValidationError('This username is already taken. Please choose another.')
        
        return username


class SendMessageForm(forms.Form):
    """Form for sending anonymous messages"""
    message_text = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Type your anonymous message here... (max 500 characters)',
            'rows': 5,
            'maxlength': 500
        })
    )
    
    def clean_message_text(self):
        message = self.cleaned_data['message_text'].strip()
        
        if len(message) < 1:
            raise ValidationError('Message cannot be empty.')
        
        # Basic spam detection
        spam_words = ['viagra', 'casino', 'lottery', 'winner']
        if any(word in message.lower() for word in spam_words):
            raise ValidationError('Your message contains prohibited content.')
        
        return message


class PinAuthForm(forms.Form):
    """Form for PIN authentication"""
    pin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg text-center',
            'placeholder': '••••',
            'maxlength': 4,
            'autocomplete': 'off',
            'inputmode': 'numeric'
        })
    )
    
    def clean_pin(self):
        pin = self.cleaned_data['pin']
        
        if not pin.isdigit():
            raise ValidationError('PIN must be 4 digits.')
        
        return pin


class LoginForm(forms.Form):
    """Form for user login"""
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your username',
            'autocomplete': 'username'
        })
    )
    
    pin = forms.CharField(
        max_length=4,
        min_length=4,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Enter your 4-digit PIN',
            'maxlength': 4,
            'autocomplete': 'current-password',
            'inputmode': 'numeric'
        })
    )
    
    def clean_username(self):
        username = self.cleaned_data['username'].lower().strip()
        return username
    
    def clean_pin(self):
        pin = self.cleaned_data['pin']
        
        if not pin.isdigit():
            raise ValidationError('PIN must be 4 digits.')
        
        return pin
