from django.urls import path
from . import views

urlpatterns = [
    path(
        'questions/<int:npc_id>/<int:location_id>/',
        views.NPCQuestionsByLocationView.as_view(),
        name='npc-questions-by-location',
    ),
    path(
        'generate-dialog/',
        views.GenerateDialogAPIView.as_view(),
        name='generate-dialog',
    ),
]
