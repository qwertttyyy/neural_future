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


class CustomUser(AbstractUser):
    icon = models.FileField(
        upload_to="users_icons/",
        validators=[SVGOrRasterImageValidator()],
        null=True,
        blank=True,
    )
    weapon = models.OneToOneField(
        Weapon, on_delete=models.SET_NULL, null=True, blank=True
    )
