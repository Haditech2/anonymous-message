"""
ASGI config for anonymous_msg project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'anonymous_msg.settings')

application = get_asgi_application()
