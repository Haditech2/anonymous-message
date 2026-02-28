# Quick Setup Guide

## 1. Install Dependencies

```bash
cd kogiuncovered-django
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## 2. Create .env File

Create `.env` file with:
```
SECRET_KEY=your-django-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://neondb_owner:npg_LW7PGxMprqZ0@ep-misty-mouse-air5052r-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
CLOUDINARY_CLOUD_NAME=ded3xrpof
CLOUDINARY_API_KEY=724112677748272
CLOUDINARY_API_SECRET=DTIYizyqgyO9bNgvKNNRAeNvZEA
ALLOWED_HOSTS=localhost,127.0.0.1,.vercel.app,.kogiuncovered.online
```

## 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 4. Create Superuser

```bash
python manage.py createsuperuser
```

## 5. Create Static Directory

```bash
mkdir static
```

## 6. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

## 7. Run Server

```bash
python manage.py runserver
```

Visit:
- Site: http://localhost:8000
- Admin: http://localhost:8000/admin

## Deploy to Vercel

```bash
vercel
```

Add environment variables in Vercel dashboard, then deploy!

## Key Features

✅ Full blog with CRUD
✅ Rich text editor
✅ Cloudinary images
✅ Comments & Likes
✅ Search functionality
✅ Admin panel
✅ Responsive design
✅ Google AdSense ready

Much simpler than React + Flask!
