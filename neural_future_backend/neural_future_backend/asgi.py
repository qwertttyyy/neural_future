import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "neural_future_backend.settings"
)
django_asgi = get_asgi_application()

from game.middleware import TokenAuthMiddleware
from game.routing import websocket_urlpatterns


application = ProtocolTypeRouter(
    {
        'http': django_asgi,
        'websocket': TokenAuthMiddleware(URLRouter(websocket_urlpatterns)),
    }
)
