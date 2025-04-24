from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Question
from .serializers import QuestionSerializer


class NPCQuestionsByLocationView(APIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get(self, request, npc_id, location_id):
        questions = Question.objects.filter(
            npc_id=npc_id, location_id=location_id
        )
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
