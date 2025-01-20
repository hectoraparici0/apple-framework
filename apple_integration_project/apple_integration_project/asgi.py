"""
ASGI config for apple_integration_project project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_integration_project.settings')
application = get_asgi_application()
