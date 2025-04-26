from django.urls import path
from rest_framework.authtoken import views as auth_views

from . import views

urlpatterns = [
    path('auth/', auth_views.obtain_auth_token),
    path("register/", views.RegisterAPIView.as_view(), name="register"),
    path("me/", views.PlayerMeAPIView.as_view(), name="player-me"),
]
