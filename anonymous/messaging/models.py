from django.db import models
from django.utils import timezone
import random
import hashlib


class UserProfile(models.Model):
    """User profile with username and PIN-based authentication"""
    username = models.CharField(max_length=50, unique=True, db_index=True)
    pin = models.CharField(max_length=4)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.username
    
    @staticmethod
    def generate_pin():
        """Generate a random 4-digit PIN"""
        return str(random.randint(1000, 9999))
    
    def get_profile_url(self):
        """Get the shareable profile URL"""
        return f"/u/{self.username}/"
    
    def get_dashboard_url(self):
        """Get the dashboard URL"""
        return f"/dashboard/{self.username}/"


class Message(models.Model):
    """Anonymous message sent to a user"""
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='messages')
    message_text = models.TextField(max_length=500)
    timestamp = models.DateTimeField(default=timezone.now)
    sender_ip_hash = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Message to {self.user.username} at {self.timestamp}"
    
    @staticmethod
    def hash_ip(ip_address):
        """Hash IP address for privacy"""
        return hashlib.sha256(ip_address.encode()).hexdigest()
    
    def mark_as_read(self):
        """Mark message as read"""
        self.status = 'read'
        self.save()


class BlockedIP(models.Model):
    """Blocked IP addresses for spam prevention"""
    ip_hash = models.CharField(max_length=64, unique=True)
    blocked_at = models.DateTimeField(default=timezone.now)
    reason = models.CharField(max_length=200, default='Spam')
    
    def __str__(self):
        return f"Blocked IP at {self.blocked_at}"
