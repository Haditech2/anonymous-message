# Anonymous Messaging Platform

A Django-based web application that allows users to receive anonymous messages. Users create a profile with a unique username, get a shareable link, and can view messages through a PIN-protected dashboard.

## Features

- **Simple Profile Creation**: Create a profile with just a username
- **PIN-Based Authentication**: Secure 4-digit PIN for dashboard access
- **Anonymous Messaging**: Anyone can send messages without revealing their identity
- **Rate Limiting**: Built-in spam protection (5 messages per minute per IP)
- **IP Blocking**: Automatic spam prevention system
- **Message Management**: View, delete individual messages, or clear all at once
- **Analytics Dashboard**: Track total messages, daily messages, and weekly trends
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default, easily switchable to PostgreSQL/MySQL)
- **Rate Limiting**: django-ratelimit
- **Image Processing**: Pillow
- **Frontend**: HTML, CSS, JavaScript (vanilla)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd anonymous_msg
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create a superuser (optional, for admin access):
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Open your browser and navigate to:
   - Homepage: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

### Creating a Profile

1. Visit the homepage
2. Enter a unique username
3. Click "Create Profile"
4. Save your 4-digit PIN (shown only once!)
5. Share your profile link with others

### Sending Anonymous Messages

1. Visit someone's profile link (e.g., `/u/username/`)
2. Type your anonymous message (max 500 characters)
3. Click "Send Message"
4. Your message is delivered anonymously

### Viewing Messages

1. Go to your dashboard (`/dashboard/username/`)
2. Enter your 4-digit PIN
3. View all received messages
4. Delete individual messages or clear all at once

## Project Structure

```
anonymous_msg/
├── anonymous_msg/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── messaging/              # Main app
│   ├── models.py          # UserProfile, Message, BlockedIP models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   ├── urls.py            # URL routing
│   └── admin.py           # Admin configuration
├── templates/              # HTML templates
│   ├── base.html
│   ├── includes/
│   └── messaging/
├── static/                 # Static files
│   ├── css/
│   └── js/
├── manage.py
└── requirements.txt
```

## Security Features

- **PIN Protection**: Dashboard access requires 4-digit PIN
- **IP Hashing**: Sender IPs are hashed (SHA-256) for privacy
- **Rate Limiting**: 5 messages per minute per IP address
- **Spam Prevention**: IP blocking system for abusive users
- **CSRF Protection**: Django's built-in CSRF protection
- **Session Management**: 24-hour session timeout

## Configuration

### Production Deployment

Before deploying to production, update `settings.py`:

1. Set `DEBUG = False`
2. Change `SECRET_KEY` to a secure random string
3. Update `ALLOWED_HOSTS` with your domain
4. Configure a production database (PostgreSQL recommended)
5. Set up static file serving
6. Enable HTTPS

### Environment Variables (Recommended)

```python
import os
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split(',')
```

## API Endpoints

- `GET /` - Homepage (create profile)
- `GET /u/<username>/` - Public profile page
- `POST /u/<username>/send/` - Send message (AJAX)
- `GET /dashboard/<username>/` - User dashboard
- `GET /dashboard/<username>/auth/` - PIN authentication
- `POST /dashboard/<username>/delete/<message_id>/` - Delete message
- `POST /dashboard/<username>/delete-all/` - Delete all messages
- `GET /dashboard/<username>/logout/` - Logout

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions, please open an issue on the repository.

---

Built with Django ❤️
