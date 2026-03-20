from django.contrib import admin
from .models import QuizAttempt, AttemptAnswer


class AttemptAnswerInline(admin.TabularInline):
    model = AttemptAnswer
    extra = 0
    readonly_fields = ('question', 'selected_option', 'is_correct')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'status', 'started_at', 'completed_at')
    list_filter = ('status', 'started_at', 'completed_at')
    search_fields = ('user__username', 'quiz__topic')
    raw_id_fields = ('user', 'quiz')
    readonly_fields = ('started_at', 'completed_at')
    date_hierarchy = 'started_at'
    
    inlines = [AttemptAnswerInline]


@admin.register(AttemptAnswer)
class AttemptAnswerAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'selected_option', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('attempt__user__username',)
    raw_id_fields = ('attempt', 'question', 'selected_option')
