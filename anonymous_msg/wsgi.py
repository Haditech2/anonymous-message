"""
WSGI config for anonymous_msg project.
"""

import os
from django.core.wsgi import get_wsgi_application

# Use production settings if DJANGO_PRODUCTION environment variable is set
if os.environ.get('DJANGO_PRODUCTION'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anonymous_msg.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anonymous_msg.settings')

# This application object is used by any WSGI server configured to use this file.
application = get_wsgi_application()

# Vercel handler
app = application
