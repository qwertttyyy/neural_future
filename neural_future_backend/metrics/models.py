from django.contrib.auth import get_user_model
from django.db import models

from npc.models import Question

User = get_user_model()


class UserAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1000)

    def __str__(self):
        return f"Ответ от {self.user.username} на вопрос от '{self.question.npc.name}' в {self.question.location.name}: {self.answer[:50]}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question', 'user'], name='unique-user-answer'
            )
        ]


class NNAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.TextField()


class SystemPromt(models.Model):
    name = models.CharField(max_length=100, unique=True)
    text = models.TextField()
    max_tokens = models.PositiveSmallIntegerField()
