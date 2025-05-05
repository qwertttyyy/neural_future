from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.response import Response

from .models import Question
from .serializers import QuestionSerializer, GenerateDialogSerializer


@extend_schema(tags=['NPC'])
class NPCQuestionsByLocationView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def list(self, request, *args, **kwargs):
        npc_id = self.kwargs['npc_id']
        location_id = self.kwargs['location_id']
        queryset = self.get_queryset().filter(
            npc_id=npc_id, location_id=location_id
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['NPC'])
class GenerateDialogAPIView(generics.CreateAPIView):

    def create(self, request, *args, **kwargs):
        serializer = GenerateDialogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_202_ACCEPTED)
