from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from metrics.models import UserAnswer
from metrics.schemas import (
    user_answer_create_schema,
    user_answer_single_create_schema,
)
from metrics.serializers import (
    UserAnswerSerializer,
    UserAnswerSingleCreateSerializer,
)


@extend_schema(tags=['Ответы'], **user_answer_create_schema)
class UserAnswerBulkCreateAPIView(generics.CreateAPIView):
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


@extend_schema(tags=['Ответы'], **user_answer_single_create_schema)
class UserAnswerSingleCreateAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserAnswerSingleCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response({"color": result}, status=status.HTTP_200_OK)
