from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, parsers

from .serializers import (
    UserRegisterSerializer,
    PlayerSerializer,
    PlayerUpdateSerializer,
)


@extend_schema(tags=["Игроки"])
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["Игроки"])
class PlayerMeAPIView(generics.RetrieveUpdateAPIView):

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [
        parsers.JSONParser,
        parsers.MultiPartParser,
        parsers.FormParser,
    ]

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ("PATCH", "PUT"):
            return PlayerUpdateSerializer
        return PlayerSerializer
