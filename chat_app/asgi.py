"""
ASGI config for chat_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator


import base.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_app.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
   "http" : django_asgi_app,
   # just HTTP for now (we can add other protocols later)
   "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(base.routing.websocket_urlpatterns))
        ),
})
