from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class NPC(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Question(models.Model):
    npc = models.ForeignKey(NPC, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    question = models.CharField(max_length=1000)

    def __str__(self):
        return f"Вопрос от '{self.npc.name}' в {self.location.name}: {self.question[:50]}"


class AnswerVariant(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name='answers'
    )
    variant = models.CharField(max_length=1000)
