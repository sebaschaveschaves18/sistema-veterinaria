"""
ASGI config for veterinaria_backend project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'veterinaria_backend.settings')

application = get_asgi_application()
