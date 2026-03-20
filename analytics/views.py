from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Avg, Max, Count
from django.core.cache import cache

from core.models import QuizAttempt
from .models import UserPerformance, TopicPerformance
from .services import get_topic_leaderboard, get_all_topics

# Cache timeout in seconds
CACHE_TIMEOUT = 60  # 1 minute for leaderboards (they change frequently)


class UserStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        topic = request.query_params.get('topic')
        
        if topic:
            # Get topic-specific stats
            try:
                performance = TopicPerformance.objects.get(user=user, topic__iexact=topic)
                return Response({
                    "topic": performance.topic,
                    "total_attempts": performance.total_attempts,
                    "avg_score": round(performance.avg_score, 2),
                    "best_score": performance.best_score,
                    "elo_points": performance.elo_points,
                    "rank": performance.rank,
                })
            except TopicPerformance.DoesNotExist:
                return Response({
                    "topic": topic,
                    "total_attempts": 0,
                    "avg_score": 0,
                    "best_score": 0,
                    "elo_points": 1000,
                    "rank": None,
                })
        else:
            # Get overall stats
            try:
                performance = UserPerformance.objects.get(user=user)
                return Response({
                    "total_attempts": performance.total_attempts,
                    "avg_score": round(performance.avg_score, 2),
                    "best_score": performance.best_score,
                    "elo_points": performance.elo_points,
                    "rank": performance.rank,
                })
            except UserPerformance.DoesNotExist:
                return Response({
                    "total_attempts": 0,
                    "avg_score": 0,
                    "best_score": 0,
                    "elo_points": 1000,
                    "rank": None,
                })


class LeaderboardView(APIView):
    """
    Global leaderboard - overall rankings across all topics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Try to get from cache first
        cache_key = 'global_leaderboard'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        # Use select_related to avoid N+1 queries
        top_users = UserPerformance.objects.select_related('user').order_by('-elo_points')[:10]
        
        leaderboard = []
        for rank, perf in enumerate(top_users, 1):
            leaderboard.append({
                "rank": rank,
                "username": perf.user.username,
                "elo_points": perf.elo_points,
                "avg_score": round(perf.avg_score, 2),
                "total_attempts": perf.total_attempts,
            })
        
        # Cache the result
        try:
            cache.set(cache_key, leaderboard, CACHE_TIMEOUT)
        except:
            pass  # Cache might not be available
        
        return Response(leaderboard)


class TopicLeaderboardView(APIView):
    """
    Topic-specific leaderboard - like LeetCode problem set rankings.
    Example: /api/analytics/leaderboard/Python/ shows Python topic rankings
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, topic):
        # Try to get from cache first
        cache_key = f'topic_leaderboard_{topic.lower()}'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        top_users = get_topic_leaderboard(topic, limit=10)
        
        leaderboard = []
        for perf in top_users:
            leaderboard.append({
                "rank": perf.rank,
                "username": perf.user.username,
                "elo_points": perf.elo_points,
                "avg_score": round(perf.avg_score, 2),
                "best_score": perf.best_score,
                "total_attempts": perf.total_attempts,
            })
        
        response_data = {
            "topic": topic,
            "leaderboard": leaderboard
        }
        
        # Cache the result
        try:
            cache.set(cache_key, response_data, CACHE_TIMEOUT)
        except:
            pass
        
        return Response(response_data)


class TopicsListView(APIView):
    """
    Get list of all available topics.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Try to get from cache first
        cache_key = 'all_topics'
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            return Response(cached_data)
        
        topics = list(get_all_topics())
        response_data = {"topics": topics}
        
        # Cache for longer (topics don't change often)
        try:
            cache.set(cache_key, response_data, CACHE_TIMEOUT * 10)
        except:
            pass
        
        return Response(response_data)


class QuizHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        topic = request.query_params.get('topic')
        page = int(request.query_params.get('page', 1))
        page_size = 20
        
        # Try to get from cache
        cache_key = f'quiz_history_{request.user.id}_page_{page}'
        if topic:
            cache_key = f'quiz_history_{request.user.id}_{topic}_page_{page}'
        
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)
        
        attempts = QuizAttempt.objects.filter(
            user=request.user
        ).select_related('quiz')
        
        if topic:
            attempts = attempts.filter(quiz__topic__iexact=topic)
        
        # Apply pagination manually since we're using APIView
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        attempts = attempts.order_by('-started_at')[start_idx:end_idx]
        
        history = []
        for attempt in attempts:
            history.append({
                "quiz_topic": attempt.quiz.topic,
                "quiz_difficulty": attempt.quiz.difficulty,
                "score": attempt.score,
                "status": attempt.status,
                "started_at": attempt.started_at,
                "completed_at": attempt.completed_at,
            })
        
        # Cache the result
        try:
            cache.set(cache_key, history, CACHE_TIMEOUT)
        except:
            pass
        
        return Response(history)
