from django.contrib import admin
from .models import UserPerformance, TopicPerformance


@admin.register(UserPerformance)
class UserPerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_attempts', 'avg_score', 'best_score', 'elo_points', 'rank', 'last_attempt_at')
    list_filter = ('rank', 'last_attempt_at')
    search_fields = ('user__username',)
    readonly_fields = ('last_attempt_at',)
    raw_id_fields = ('user',)
    date_hierarchy = 'last_attempt_at'


@admin.register(TopicPerformance)
class TopicPerformanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'total_attempts', 'avg_score', 'best_score', 'elo_points', 'rank', 'last_attempt_at')
    list_filter = ('topic', 'rank', 'last_attempt_at')
    search_fields = ('user__username', 'topic')
    readonly_fields = ('last_attempt_at',)
    raw_id_fields = ('user',)
    date_hierarchy = 'last_attempt_at'
