from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django_ratelimit.decorators import ratelimit
from .models import UserProfile, Message, BlockedIP
from .forms import CreateProfileForm, SendMessageForm, PinAuthForm, LoginForm
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_ip_blocked(ip_address):
    """Check if IP is blocked"""
    ip_hash = Message.hash_ip(ip_address)
    return BlockedIP.objects.filter(ip_hash=ip_hash).exists()


def index(request):
    """Homepage - Create profile"""
    if request.method == 'POST':
        form = CreateProfileForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pin = UserProfile.generate_pin()
            
            # Create user profile
            user_profile = UserProfile.objects.create(
                username=username,
                pin=pin
            )
            
            # Store in session
            request.session['created_username'] = username
            request.session['created_pin'] = pin
            
            return redirect('profile_created')
    else:
        form = CreateProfileForm()
    
    return render(request, 'messaging/index.html', {'form': form})


def profile_created(request):
    """Show created profile details with PIN"""
    username = request.session.get('created_username')
    pin = request.session.get('created_pin')
    
    if not username or not pin:
        return redirect('index')
    
    user_profile = get_object_or_404(UserProfile, username=username)
    
    # Clear session after showing once
    if request.GET.get('clear') == '1':
        del request.session['created_username']
        del request.session['created_pin']
        return redirect('index')
    
    context = {
        'user_profile': user_profile,
        'pin': pin,
        'profile_url': request.build_absolute_uri(user_profile.get_profile_url()),
    }
    
    return render(request, 'messaging/profile_created.html', context)


def public_profile(request, username):
    """Public profile page where anyone can send anonymous messages"""
    user_profile = get_object_or_404(UserProfile, username=username)
    
    if request.method == 'POST':
        return send_message_ajax(request, username)
    
    form = SendMessageForm()
    
    context = {
        'user_profile': user_profile,
        'form': form,
    }
    
    return render(request, 'messaging/public_send.html', context)


@ratelimit(key='ip', rate='5/m', method='POST')
@require_http_methods(["POST"])
def send_message_ajax(request, username):
    """AJAX endpoint for sending messages"""
    was_limited = getattr(request, 'limited', False)
    
    if was_limited:
        return JsonResponse({
            'success': False,
            'error': 'Too many messages. Please wait a moment.'
        }, status=429)
    
    # Check if IP is blocked
    ip_address = get_client_ip(request)
    if is_ip_blocked(ip_address):
        return JsonResponse({
            'success': False,
            'error': 'Your IP has been blocked due to spam.'
        }, status=403)
    
    user_profile = get_object_or_404(UserProfile, username=username)
    form = SendMessageForm(request.POST)
    
    if form.is_valid():
        message_text = form.cleaned_data['message_text']
        
        # Create message
        message = Message.objects.create(
            user=user_profile,
            message_text=message_text,
            sender_ip_hash=Message.hash_ip(ip_address)
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Your anonymous message has been sent! 🎉'
        })
    else:
        errors = form.errors.as_json()
        return JsonResponse({
            'success': False,
            'error': 'Please check your message and try again.',
            'errors': errors
        }, status=400)


def dashboard_auth(request, username):
    """PIN authentication for dashboard access"""
    user_profile = get_object_or_404(UserProfile, username=username)
    
    # Check if already authenticated
    if request.session.get(f'auth_{username}') == True:
        return redirect('dashboard', username=username)
    
    if request.method == 'POST':
        form = PinAuthForm(request.POST)
        if form.is_valid():
            pin = form.cleaned_data['pin']
            
            if pin == user_profile.pin:
                # Set session
                request.session[f'auth_{username}'] = True
                return redirect('dashboard', username=username)
            else:
                messages.error(request, 'Incorrect PIN. Please try again.')
    else:
        form = PinAuthForm()
    
    context = {
        'user_profile': user_profile,
        'form': form,
    }
    
    return render(request, 'messaging/dashboard_auth.html', context)


def dashboard(request, username):
    """User dashboard - view messages"""
    user_profile = get_object_or_404(UserProfile, username=username)
    
    # Check authentication
    if not request.session.get(f'auth_{username}'):
        return redirect('dashboard_auth', username=username)
    
    # Get messages
    messages_list = user_profile.messages.all()
    
    # Mark all as read
    messages_list.filter(status='unread').update(status='read')
    
    # Analytics
    total_messages = messages_list.count()
    today = timezone.now().date()
    today_messages = messages_list.filter(timestamp__date=today).count()
    
    # Last 7 days messages
    week_ago = timezone.now() - timedelta(days=7)
    week_messages = messages_list.filter(timestamp__gte=week_ago).count()
    
    context = {
        'user_profile': user_profile,
        'messages': messages_list,
        'total_messages': total_messages,
        'today_messages': today_messages,
        'week_messages': week_messages,
        'profile_url': request.build_absolute_uri(user_profile.get_profile_url()),
    }
    
    return render(request, 'messaging/dashboard.html', context)


@require_http_methods(["POST"])
def delete_message(request, username, message_id):
    """Delete a single message"""
    user_profile = get_object_or_404(UserProfile, username=username)
    
    # Check authentication
    if not request.session.get(f'auth_{username}'):
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=403)
    
    message = get_object_or_404(Message, id=message_id, user=user_profile)
    message.delete()
    
    return JsonResponse({'success': True, 'message': 'Message deleted'})


@require_http_methods(["POST"])
def delete_all_messages(request, username):
    """Delete all messages"""
    user_profile = get_object_or_404(UserProfile, username=username)
    
    # Check authentication
    if not request.session.get(f'auth_{username}'):
        return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=403)
    
    count = user_profile.messages.count()
    user_profile.messages.all().delete()
    
    return JsonResponse({'success': True, 'message': f'{count} messages deleted'})


def logout_dashboard(request, username):
    """Logout from dashboard"""
    if f'auth_{username}' in request.session:
        del request.session[f'auth_{username}']
    
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def login(request):
    """Login page for existing users"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            pin = form.cleaned_data['pin']
            
            try:
                user_profile = UserProfile.objects.get(username=username)
                
                if pin == user_profile.pin:
                    # Set session
                    request.session[f'auth_{username}'] = True
                    messages.success(request, f'Welcome back, @{username}!')
                    return redirect('dashboard', username=username)
                else:
                    messages.error(request, 'Incorrect PIN. Please try again.')
            except UserProfile.DoesNotExist:
                messages.error(request, 'Username not found. Please check and try again.')
    else:
        form = LoginForm()
    
    return render(request, 'messaging/login.html', {'form': form})


def generate_message_image(request, username, message_id):
    """Generate an image for a message to share on social media"""
    user_profile = get_object_or_404(UserProfile, username=username)
    
    # Check authentication
    if not request.session.get(f'auth_{username}'):
        return HttpResponse('Unauthorized', status=403)
    
    message = get_object_or_404(Message, id=message_id, user=user_profile)
    
    # Create image
    width, height = 1080, 1080
    bg_color = (88, 101, 242)  # Discord-like blue
    text_color = (255, 255, 255)
    accent_color = (255, 255, 255, 50)
    
    # Create image with gradient-like background
    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # Add decorative elements
    draw.ellipse([width-300, -150, width+150, 300], fill=accent_color)
    draw.ellipse([-150, height-300, 300, height+150], fill=accent_color)
    
    # Try to use fonts, with multiple fallbacks - using very large, highly readable sizes
    try:
        # Try Windows fonts with very large sizes
        title_font = ImageFont.truetype("arial.ttf", 90)
        message_font = ImageFont.truetype("arialbd.ttf", 72)  # Bold for better readability
        footer_font = ImageFont.truetype("arial.ttf", 50)
        small_font = ImageFont.truetype("arial.ttf", 40)
    except:
        try:
            # Try alternative Windows fonts with very large sizes
            title_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 90)
            message_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 72)
            footer_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 50)
            small_font = ImageFont.truetype("C:\\Windows\\Fonts\\arial.ttf", 40)
        except:
            try:
                # Try Linux fonts with very large sizes
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 90)
                message_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
                footer_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
            except:
                # Use default font as last resort
                title_font = ImageFont.load_default()
                message_font = ImageFont.load_default()
                footer_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
    
    # Add title
    title_text = "📨 Anonymous Message"
    try:
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 100), title_text, fill=text_color, font=title_font)
    except:
        # Fallback without emoji
        title_text = "Anonymous Message"
        title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
        draw.text(((width - title_width) // 2, 100), title_text, fill=text_color, font=title_font)
    
    # Add decorative line
    draw.rectangle([width//2 - 180, 230, width//2 + 180, 242], fill=text_color)
    
    # Wrap and add message text - adjusted for much larger font
    max_chars = 22  # Further reduced to accommodate much larger font
    wrapped_lines = textwrap.wrap(message.message_text, width=max_chars)
    
    # Limit to 8 lines for very large font
    if len(wrapped_lines) > 8:
        wrapped_lines = wrapped_lines[:8]
        wrapped_lines[-1] = wrapped_lines[-1][:max_chars-3] + "..."
    
    y_offset = 350
    line_height = 85  # Much larger spacing for very large text
    
    for line in wrapped_lines:
        line_bbox = draw.textbbox((0, 0), line, font=message_font)
        line_width = line_bbox[2] - line_bbox[0]
        draw.text(((width - line_width) // 2, y_offset), line, fill=text_color, font=message_font)
        y_offset += line_height
    
    # Add footer
    footer_text = f"Sent to @{username}"
    footer_bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
    footer_width = footer_bbox[2] - footer_bbox[0]
    draw.text(((width - footer_width) // 2, height - 200), footer_text, fill=text_color, font=footer_font)
    
    # Add website/call to action
    cta_text = "Send me anonymous messages!"
    cta_bbox = draw.textbbox((0, 0), cta_text, font=small_font)
    cta_width = cta_bbox[2] - cta_bbox[0]
    draw.text(((width - cta_width) // 2, height - 100), cta_text, fill=(255, 255, 255, 200), font=small_font)
    
    # Save to bytes
    img_io = io.BytesIO()
    img.save(img_io, 'PNG', quality=95)
    img_io.seek(0)
    
    response = HttpResponse(img_io, content_type='image/png')
    response['Content-Disposition'] = f'inline; filename="message_{message_id}.png"'
    return response
