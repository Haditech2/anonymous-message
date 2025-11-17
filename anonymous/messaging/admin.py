from django.contrib import admin
from .models import UserProfile, Message, BlockedIP


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'pin', 'created_at', 'message_count']
    search_fields = ['username']
    readonly_fields = ['created_at']
    
    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message_preview', 'status', 'timestamp']
    list_filter = ['status', 'timestamp']
    search_fields = ['user__username', 'message_text']
    readonly_fields = ['timestamp', 'sender_ip_hash']
    
    def message_preview(self, obj):
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    message_preview.short_description = 'Message'


@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ['ip_hash', 'reason', 'blocked_at']
    list_filter = ['blocked_at']
    readonly_fields = ['blocked_at']
