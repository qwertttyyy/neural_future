from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from metrics.models import UserAnswer
from metrics.schemas import user_answer_create_schema
from metrics.serializers import UserAnswerSerializer


@extend_schema(tags=['Ответы'], **user_answer_create_schema)
class UserAnswerCreateAPIView(generics.CreateAPIView):
    queryset = UserAnswer.objects.select_related(
        'user',
        'question',
    )
    serializer_class = UserAnswerSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
