from django.urls import path
from . import views

urlpatterns = [
    path(
        'user-answers/single/color/',
        views.UserAnswerSingleColorCreateAPIView.as_view(),
        name='user-answer-single',
    ),
    path(
        'user-answers/single/forms/',
        views.UserAnswerSingleFormsCreateAPIView.as_view(),
        name='user-answer-single-forms',
    ),
    path(
        'user-answers/multiple/',
        views.UserAnswerBulkCreateAPIView.as_view(),
        name='user-answer-bulk',
    ),
]
