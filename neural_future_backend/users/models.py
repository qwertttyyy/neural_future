from django.contrib.auth.models import AbstractUser
from django.db import models


class Weapon(models.Model):
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='weapons/')
    width = models.PositiveSmallIntegerField()
    height = models.PositiveSmallIntegerField()
    damage = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    icon = models.ImageField(null=True, blank=True, upload_to='users_icons/')
    weapon = models.OneToOneField(
        Weapon, on_delete=models.SET_NULL, null=True, blank=True
    )
