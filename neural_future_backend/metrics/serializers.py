from django.db import transaction
from rest_framework import serializers

from metrics.models import UserAnswer
from npc.models import Location
from npc.serializers import QuestionSerializer


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserAnswerListSerializer(serializers.ListSerializer):

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        answers = []
        for item in validated_data:
            qa, created = UserAnswer.objects.update_or_create(
                user=user,
                question=item['question'],
                defaults={'answer': item['answer']},
            )
            answers.append(qa)
        return answers


class UserAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserAnswer
        fields = ('question', 'answer')
        list_serializer_class = UserAnswerListSerializer
