from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.http import Http404
from django.db.models import Prefetch
from django.core.cache import cache

from quizzes.models import Quiz, QuestionOption
from .models import QuizAttempt, AttemptAnswer

from analytics.services import update_user_performance


class StartQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quiz_id):
        try:
            quiz = Quiz.objects.get(id=quiz_id)
        except Quiz.DoesNotExist:
            return Response(
                {"error": "Quiz not found"},
                status=404
            )

        attempt, created = QuizAttempt.objects.get_or_create(
            user=request.user,
            quiz=quiz
        )

        return Response({
            "attempt_id": attempt.id,
            "status": attempt.status,
            "created": created
        })
    

class SubmitAnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        # Validate request data - support both field names
        question_id = request.data.get("question_id")
        option_id = request.data.get("option_id") or request.data.get("selected_option_id")
        
        if not question_id or not option_id:
            return Response(
                {"error": "question_id and option_id (or selected_option_id) are required"},
                status=400
            )

        try:
            attempt = QuizAttempt.objects.select_related('quiz').get(id=attempt_id, user=request.user)
        except QuizAttempt.DoesNotExist:
            return Response(
                {"error": "Attempt not found or not owned by user"},
                status=404
            )

        try:
            option = QuestionOption.objects.get(id=option_id, question_id=question_id)
        except QuestionOption.DoesNotExist:
            return Response(
                {"error": "Option not found for this question"},
                status=404
            )

        is_correct = option.is_correct

        AttemptAnswer.objects.update_or_create(
            attempt=attempt,
            question_id=question_id,
            defaults={
                "selected_option_id": option_id,
                "is_correct": is_correct
            }
        )

        # Invalidate history cache after answering
        try:
            cache.delete(f'quiz_history_{request.user.id}_page_1')
        except:
            pass  # Cache might not be available

        return Response({"is_correct": is_correct, "correct_answer": option.id})
    

class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, attempt_id):
        try:
            attempt = QuizAttempt.objects.select_related('quiz').get(id=attempt_id, user=request.user)
        except QuizAttempt.DoesNotExist:
            return Response(
                {"error": "Attempt not found or not owned by user"},
                status=404
            )

        # Use optimized query
        answers = attempt.answers.all()
        total_questions = answers.count()
        correct_answers = sum(1 for a in answers if a.is_correct)

        # Calculate score as percentage
        score = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        attempt.score = score
        attempt.status = "completed"
        attempt.completed_at = timezone.now()
        attempt.save()

        # Update performance with topic (like LeetCode problem sets)
        update_user_performance(
            user=request.user,
            score=score,
            topic=attempt.quiz.topic
        )

        # Clear caches after quiz completion
        try:
            cache.delete(f'quiz_history_{request.user.id}_page_1')
            cache.delete('global_leaderboard')
            cache.delete(f'topic_leaderboard_{attempt.quiz.topic.lower()}')
        except:
            pass  # Cache might not be available
        cache.delete('all_topics')

        return Response({
            "score": score,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "status": attempt.status
        })
