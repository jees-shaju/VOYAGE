from django.contrib import admin
from .models import Score


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('username', 'seconds_wasted', 'created_at')
    search_fields = ('username',)
    list_filter = ('created_at',)
    ordering = ('-seconds_wasted',)
