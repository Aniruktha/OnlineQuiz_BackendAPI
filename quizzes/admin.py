from django.contrib import admin
from .models import Quiz, Question, QuestionOption


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1
    fields = ('option_text', 'is_correct')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    inlines = [QuestionOptionInline]


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('topic', 'difficulty', 'created_by', 'created_at')
    list_filter = ('difficulty', 'created_at')
    search_fields = ('topic',)
    readonly_fields = ('created_at',)
    raw_id_fields = ('created_by',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Quiz Information', {
            'fields': ('topic', 'difficulty', 'created_by', 'created_at')
        }),
    )
    
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'id')
    list_filter = ('quiz',)
    search_fields = ('text',)
    raw_id_fields = ('quiz',)


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('option_text', 'question', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('option_text',)
    raw_id_fields = ('question',)
