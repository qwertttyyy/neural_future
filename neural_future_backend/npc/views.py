from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.response import Response

from .models import Question
from .serializers import QuestionSerializer


@extend_schema(tags=['Вопросы NPC'])
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

    # def get(self, request, npc_id, location_id):
    #     questions = Question.objects.filter(
    #         npc_id=npc_id, location_id=location_id
    #     )
    #     serializer = QuestionSerializer(questions, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
