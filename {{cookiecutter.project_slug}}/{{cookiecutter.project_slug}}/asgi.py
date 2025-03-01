import os
import sys
from pathlib import Path

from django.urls import path
from channels.routing import URLRouter, ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{{ cookiecutter.project_slug }}.settings')

application = get_asgi_application()

# Add your routing here
# Example:
# ws_router = URLRouter([
#     path("ws/notifications/", NotificationConsumer.as_asgi()),
# ])

# application = ProtocolTypeRouter({
#     "http": application,
#     "websocket": AllowedHostsOriginValidator(ws_router),
# })
