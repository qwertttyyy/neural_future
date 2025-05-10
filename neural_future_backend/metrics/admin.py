from django.contrib import admin

from metrics.models import UserAnswer, SystemPromt


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'answer')


@admin.register(SystemPromt)
class SystemPromtAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_text", "max_tokens")
    search_fields = ("name", "text")
    list_display_links = ("id", "name")
    list_editable = ("max_tokens",)
    ordering = ("name",)

    def short_text(self, obj):
        return (obj.text[:60] + "…") if len(obj.text) > 60 else obj.text

    short_text.short_description = "Текст промта"
