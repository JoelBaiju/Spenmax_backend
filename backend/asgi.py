"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# application = get_asgi_application()



from channels.routing import ProtocolTypeRouter, URLRouter
import os
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import OriginValidator , AllowedHostsOriginValidator
# from notification.AllowedHost import CustomAllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

asgi_application = get_asgi_application() #new

import notification.routing 

application = ProtocolTypeRouter({
                "http": asgi_application,
                "websocket": 
                    # AllowedHostsOriginValidator(
                        AuthMiddlewareStack(
                            URLRouter(notification.routing.websocket_urlpatterns) 
                        )
                    # )
            })