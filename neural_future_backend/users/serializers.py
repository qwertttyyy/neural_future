from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import Weapon, CharacterClass

User = get_user_model()


class WeaponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weapon
        fields = (
            "id",
            "name",
            'weapon_img',
            'projectile_img',
            'width',
            'height',
            'damage',
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
        )
        Token.objects.create(user=user)  # сразу выдаём токен
        return user


class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = ("id", "name")


class PlayerSerializer(serializers.ModelSerializer):
    weapon = WeaponSerializer(read_only=True)
    character_class = CharacterClassSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "icon",
            "weapon",
            'character_class',
            'hp',
            'experience',
            'level',
        )


class PlayerUpdateSerializer(serializers.ModelSerializer):
    weapon = serializers.PrimaryKeyRelatedField(
        queryset=Weapon.objects.all(),
        required=False,
        allow_null=True,
    )
    character_class = serializers.PrimaryKeyRelatedField(
        queryset=CharacterClass.objects.all(),
        required=False,
        allow_null=True,
    )
    icon = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "icon",
            "weapon",
            'character_class',
            'hp',
            'experience',
            'level',
        )
