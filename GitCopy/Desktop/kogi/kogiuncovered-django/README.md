# Kogiuncovered TV - Django Blog

A full-featured blog platform built with Django, PostgreSQL, and Cloudinary.

## Features

- ✅ Full blog functionality (Create, Read, Update, Delete posts)
- ✅ Rich text editor (CKEditor)
- ✅ Image uploads to Cloudinary
- ✅ Comments system
- ✅ Like system
- ✅ Tags and categories
- ✅ Responsive design
- ✅ Django Admin panel
- ✅ PostgreSQL database (Neon)
- ✅ Ready for Vercel deployment

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd kogiuncovered-django
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create .env File

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=postgresql://neondb_owner:npg_LW7PGxMprqZ0@ep-misty-mouse-air5052r-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
CLOUDINARY_CLOUD_NAME=ded3xrpof
CLOUDINARY_API_KEY=724112677748272
CLOUDINARY_API_SECRET=DTIYizyqgyO9bNgvKNNRAeNvZEA
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser

```bash
python manage.py createsuperuser
```

### 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit:
- Frontend: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## Deployment to Vercel

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel
```

3. Add environment variables in Vercel dashboard

4. Your site will be live!

## Project Structure

```
kogiuncovered-django/
├── manage.py
├── requirements.txt
├── kogiuncovered/          # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog/                   # Blog application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── templates/         # HTML templates
├── static/                # CSS, JS, images
└── templates/             # Base templates
```

## Admin Panel

Access the Django admin at `/admin` to:
- Create and manage blog posts
- Moderate comments
- View analytics
- Manage users

Much simpler than the React + Flask setup!
