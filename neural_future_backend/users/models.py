from django.contrib.auth.models import AbstractUser
from django.db import models

from core.validators import SVGOrRasterImageValidator


class Weapon(models.Model):
    name = models.CharField(max_length=100)
    img = models.FileField(
        upload_to="weapons/",
        validators=[SVGOrRasterImageValidator()],
        null=True,
        blank=True,
    )
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    damage = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    icon = models.FileField(
        upload_to="users_icons/",
        validators=[SVGOrRasterImageValidator()],
        null=True,
        blank=True,
    )
    weapon = models.ForeignKey(
        Weapon, on_delete=models.SET_NULL, null=True, blank=True
    )
    character_class = models.ForeignKey(
        CharacterClass,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    hp = models.PositiveIntegerField(
        default=100,
    )
    experience = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    story = models.TextField(blank=True, default="")

    def __str__(self):
        return self.username
