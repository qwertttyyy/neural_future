from django.urls import path
from .consumers import PlayerConsumer

websocket_urlpatterns = [
    path('ws/game/', PlayerConsumer.as_asgi()),
]
