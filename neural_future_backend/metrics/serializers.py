from django.db import transaction
from rest_framework import serializers

from metrics.models import UserAnswer
from npc.models import Location
from services.deepseek import generate_background_color, generate_forms
from .tasks import generate_story_task


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class UserAnswerListSerializer(serializers.ListSerializer):

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        answers = []
        pairs = []
        for item in validated_data:
            question = item['question']
            answer = item['answer']
            qa, created = UserAnswer.objects.update_or_create(
                user=user,
                question=question,
                defaults={'answer': answer},
            )
            answers.append(qa)
            pairs.append(f'Q: {question} A: {answer}')
        generate_story_task.delay(user_id=user.id, q_a_pairs=pairs)
        return answers


class UserAnswerSingleColorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ('question', 'answer')

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        answer = validated_data['answer']
        UserAnswer.objects.update_or_create(
            user=user, question=question, defaults={'answer': answer}
        )
        return generate_background_color(user.id, question.id, answer)


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ('question', 'answer')
        list_serializer_class = UserAnswerListSerializer


class FormsSerializer(serializers.ModelSerializer):
    body = serializers.CharField(required=True)

    class Meta:
        model = UserAnswer
        fields = ('question', 'answer', 'body')

    def create(self, validated_data):
        user = self.context['request'].user
        question = validated_data['question']
        answer = validated_data['answer']
        UserAnswer.objects.update_or_create(
            user=user, question=question, defaults={'answer': answer}
        )
        return generate_forms(
            user.id, question.id, answer, validated_data['body']
        )
