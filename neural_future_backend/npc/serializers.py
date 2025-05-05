from rest_framework import serializers

from metrics.tasks import generate_dialog_task
from npc.models import NPC, Question


class NPCSerializer(serializers.ModelSerializer):
    class Meta:
        model = NPC
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'question')


class GenerateDialogSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    npc_id = serializers.IntegerField()
    location_id = serializers.IntegerField()

    def create(self, validated_data):
        user_id = validated_data['user_id']
        npc_id = validated_data['npc_id']
        location_id = validated_data['location_id']
        generate_dialog_task.delay(user_id, npc_id, location_id)
        return {}
