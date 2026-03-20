from rest_framework import serializers
from .models import Quiz, Question, QuestionOption

class QuestionOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionOption
        # SECURITY: Don't expose is_correct to prevent answer leakage
        fields = ["id", "option_text"]
        read_only_fields = ["id", "option_text"]

class QuestionSerializer(serializers.ModelSerializer):
    options = QuestionOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ["id", "text", "options"]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "topic", "difficulty", "questions", "created_at", "created_by"]
        read_only_fields = ["id", "created_at", "created_by"]


class CreateQuizSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=255)
    question_count = serializers.IntegerField(min_value=1, max_value=20, default=5)
    difficulty = serializers.ChoiceField(
        choices=['easy', 'medium', 'hard'],
        default='medium'
    )