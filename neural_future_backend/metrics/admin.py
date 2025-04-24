from django.contrib import admin

from metrics.models import UserAnswer


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'answer')
