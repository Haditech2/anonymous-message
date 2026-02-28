from django.contrib import admin
from .models import Post, Comment, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'published')
    list_filter = ('published', 'created_at', 'author')
    search_fields = ('title', 'content', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'author', 'excerpt')
        }),
        ('Content', {
            'fields': ('content', 'featured_image', 'tags')
        }),
        ('Publishing', {
            'fields': ('published',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('author_name', 'content')
    actions = ['approve_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = 'Approve selected comments'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user_ip', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('post__title',)
