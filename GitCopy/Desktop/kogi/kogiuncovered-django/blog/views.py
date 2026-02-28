from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm


def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    """Home page with featured posts"""
    featured_posts = Post.objects.filter(published=True)[:6]
    latest_posts = Post.objects.filter(published=True)[:3]
    
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts,
    }
    return render(request, 'blog/home.html', context)


def articles_list(request):
    """List all articles"""
    posts = Post.objects.filter(published=True)
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/articles.html', context)


def article_detail(request, slug):
    """Article detail page"""
    post = get_object_or_404(Post, slug=slug, published=True)
    comments = post.comments.filter(approved=True)
    user_ip = get_client_ip(request)
    user_liked = Like.objects.filter(post=post, user_ip=user_ip).exists()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'Your comment has been posted!')
            return redirect('article_detail', slug=slug)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'likes_count': post.likes.count(),
        'comments_count': comments.count(),
    }
    return render(request, 'blog/article_detail.html', context)


@login_required
def create_post(request):
    """Create new post (admin only)"""
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to create posts.')
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('article_detail', slug=post.slug)
    else:
        form = PostForm()
    
    context = {'form': form}
    return render(request, 'blog/create_post.html', context)


@login_required
def edit_post(request, slug):
    """Edit existing post (admin only)"""
    post = get_object_or_404(Post, slug=slug)
    
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to edit posts.')
        return redirect('home')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('article_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    context = {'form': form, 'post': post}
    return render(request, 'blog/edit_post.html', context)


@login_required
def delete_post(request, slug):
    """Delete post (admin only)"""
    post = get_object_or_404(Post, slug=slug)
    
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to delete posts.')
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('articles_list')
    
    context = {'post': post}
    return render(request, 'blog/delete_confirm.html', context)


def toggle_like(request, slug):
    """Toggle like on a post"""
    post = get_object_or_404(Post, slug=slug)
    user_ip = get_client_ip(request)
    
    like, created = Like.objects.get_or_create(post=post, user_ip=user_ip)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'likes_count': post.likes.count()
        })
    
    return redirect('article_detail', slug=slug)


def search(request):
    """Search posts"""
    query = request.GET.get('q', '')
    posts = Post.objects.none()
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__icontains=query),
            published=True
        ).distinct()
    
    context = {
        'posts': posts,
        'query': query,
    }
    return render(request, 'blog/search.html', context)


def about(request):
    """About page"""
    return render(request, 'blog/about.html')


def contact(request):
    """Contact page"""
    return render(request, 'blog/contact.html')


def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'blog/privacy.html')


def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'blog/terms.html')
