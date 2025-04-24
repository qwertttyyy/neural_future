from rest_framework.authtoken import views as auth_views
from django.urls import path

urlpatterns = [
    path('auth/', auth_views.obtain_auth_token)
]