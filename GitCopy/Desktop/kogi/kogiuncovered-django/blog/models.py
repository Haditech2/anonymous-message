from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    excerpt = models.TextField(max_length=300)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    featured_image = CloudinaryField('image', blank=True, null=True)
    tags = models.CharField(max_length=200, help_text='Comma-separated tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_tags_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]
    
    def reading_time(self):
        words = len(self.content.split())
        minutes = max(1, words // 200)
        return f"{minutes} min read"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['created_at']
        
    def __str__(self):
        return f'Comment by {self.author_name} on {self.post.title}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user_ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'user_ip')
        
    def __str__(self):
        return f'Like on {self.post.title}'
