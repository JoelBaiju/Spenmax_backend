from channels.security.websocket import AllowedHostsOriginValidator
from django.conf import settings

class CustomAllowedHostsOriginValidator(AllowedHostsOriginValidator):
    async def __call__(self, scope, receive, send):
        # Get the origin from the scope
        headers = dict(scope['headers'])
        origin = headers.get(b'origin', b'').decode('utf-8')
        
        # Check if the origin is allowed based on ALLOWED_HOSTS
        if origin not in settings.ALLOWED_HOSTS:
            # If origin is not allowed, reject the connection
            await self.send_invalid_origin(scope, receive, send)
            return

        # If origin is allowed, continue with the parent class logic
        return await super().__call__(scope, receive, send)
