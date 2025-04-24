from django.urls import path
from . import views

urlpatterns = [
    path(
        'user-answer/',
        views.UserAnswerCreateAPIView.as_view(),
        name='user-answer',
    ),
]
