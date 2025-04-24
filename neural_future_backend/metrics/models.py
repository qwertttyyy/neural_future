from django.contrib.auth.models import User
from django.db import models

from npc.models import Question


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
