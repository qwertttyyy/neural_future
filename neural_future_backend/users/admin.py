# admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

from .models import Weapon

User = get_user_model()


# ────────────────────────────── Weapon ──────────────────────────────
@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "damage", "size", "preview")
    search_fields = ("name",)
    readonly_fields = ("preview",)

    def size(self, obj):
        return f"{obj.width}×{obj.height}"

    size.short_description = "Size"

    def preview(self, obj):
        if obj.img:
            return format_html(
                '<img src="{}" style="max-height:50px;" />', obj.img.url
            )
        return "—"

    preview.short_description = "Image"


# ──────────────────────── CustomUser (Player) ───────────────────────
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "weapon",
        "avatar",
        "is_staff",
        "is_active",
    )
    readonly_fields = ("avatar",)

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        ("Game data", {"fields": ("icon", "avatar", "weapon")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    def avatar(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="max-height:50px;" />', obj.icon.url
            )
        return "—"

    avatar.short_description = "Icon"
