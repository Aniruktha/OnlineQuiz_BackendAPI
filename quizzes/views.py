from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Prefetch
from django.core.cache import cache
import re

from .models import Quiz, Question, QuestionOption
from .serializers import QuizSerializer, CreateQuizSerializer
from .ai_service import generate_quiz_questions


# Cache timeout in seconds (5 minutes)
CACHE_TIMEOUT = 300


def get_unique_topic_name(topic_name):
    """
    Check if a quiz with this topic already exists.
    If it does, return a unique topic name with incremental number.
    e.g., "JavaScript" -> "JavaScript 2" -> "JavaScript 3"
    """
    # Check if topic exists exactly
    if not Quiz.objects.filter(topic=topic_name).exists():
        return topic_name
    
    # Find existing quizzes with this topic pattern
    escaped_topic = re.escape(topic_name)
    pattern = re.compile(r'^' + escaped_topic + r'(?:\s+(\d+))?$', re.IGNORECASE)
    
    max_num = 0
    existing_quizzes = Quiz.objects.filter(topic__regex=r'^' + escaped_topic + r'(?:\s+\d+)?$')
    
    for quiz in existing_quizzes:
        match = pattern.match(quiz.topic)
        if match:
            if match.group(1):
                num = int(match.group(1))
                max_num = max(max_num, num)
            else:
                max_num = max(max_num, 1)
    
    return f"{topic_name} {max_num + 1}"


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.select_related('created_by').prefetch_related(
        Prefetch('questions', queryset=Question.objects.prefetch_related('options'))
    ).all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateQuizSerializer
        return QuizSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            # Only admins can create/delete quizzes
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        topic = serializer.validated_data['topic']
        question_count = serializer.validated_data.get('question_count', 5)
        difficulty = serializer.validated_data.get('difficulty', 'medium')
        
        # Get unique topic name (add incremental number if exists)
        unique_topic = get_unique_topic_name(topic)
        
        # Generate questions using AI service
        try:
            questions_data = generate_quiz_questions(topic, question_count, difficulty)
            
            # Validate AI returned questions
            if not questions_data:
                return Response(
                    {"error": "AI failed to generate questions. Please try again with a different topic."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Create quiz with questions using the unique topic name
            quiz = Quiz.objects.create(
                topic=unique_topic,
                difficulty=difficulty,
                created_by=request.user
            )
            
            for q_data in questions_data:
                question = Question.objects.create(
                    quiz=quiz,
                    text=q_data['question']
                )
                
                for opt_data in q_data['options']:
                    QuestionOption.objects.create(
                        question=question,
                        option_text=opt_data['text'],
                        is_correct=opt_data['is_correct']
                    )
            
            output_serializer = QuizSerializer(quiz)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response(
                {"error": f"Failed to generate quiz: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def list(self, request, *args, **kwargs):
        """List quizzes with caching for better performance."""
        cache_key = f'quizzes_list_page_{request.query_params.get("page", 1)}'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        response = super().list(request, *args, **kwargs)
        
        # Cache the response data
        try:
            if response.status_code == 200:
                cache.set(cache_key, response.data, CACHE_TIMEOUT)
        except:
            pass  # Cache might not be available
        
        return response
    
    def perform_create(self, serializer):
        """Clear cache when new quiz is created."""
        serializer.save()
        try:
            cache.delete('quizzes_list_page_1')
        except:
            pass
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """Get quiz questions (without showing correct answers)"""
        quiz = self.get_object()
        # Use optimized query with prefetch
        questions = quiz.questions.prefetch_related('options').all()
        
        data = []
        for q in questions:
            data.append({
                "id": q.id,
                "text": q.text,
                "options": [
                    {"id": opt.id, "option_text": opt.option_text}
                    for opt in q.options.all()
                ]
            })
        
        return Response(data)
    
    def perform_destroy(self, instance):
        """Clear cache when quiz is deleted."""
        instance.delete()
        try:
            cache.delete_pattern('quizzes_list_*')
        except:
            pass
