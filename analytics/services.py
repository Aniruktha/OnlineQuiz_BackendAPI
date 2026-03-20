from django.utils import timezone
from django.db.models import Count
from django.core.cache import cache

from .models import UserPerformance, TopicPerformance


def update_user_performance(user, score, topic=None):
    """
    Update user performance metrics including ELO ranking.
    Updates both overall performance and topic-specific performance.
    
    Args:
        user: The user who took the quiz
        score: The score achieved (0-100)
        topic: The quiz topic (e.g., "Python", "JavaScript")
    """
    # Update overall performance
    _update_overall_performance(user, score)
    
    # Update topic-specific performance if topic provided
    if topic:
        _update_topic_performance(user, score, topic)
    
    # Clear related caches
    _clear_performance_caches(topic)


def _update_overall_performance(user, score):
    """Update overall user performance across all topics."""
    perf, created = UserPerformance.objects.get_or_create(
        user=user,
        defaults={
            'total_attempts': 0,
            'avg_score': 0,
            'best_score': 0,
            'elo_points': 1000,
        }
    )

    perf.total_attempts += 1
    perf.best_score = max(perf.best_score, score)

    # Calculate running average
    perf.avg_score = (
        (perf.avg_score * (perf.total_attempts - 1) + score)
        / perf.total_attempts
    )

    # Calculate ELO gain based on score
    elo_change = _calculate_elo_change(score)
    perf.elo_points = max(100, perf.elo_points + elo_change)
    perf.rank = _calculate_rank(perf.elo_points)
    perf.last_attempt_at = timezone.now()
    perf.save()


def _update_topic_performance(user, score, topic):
    """Update user performance for a specific topic."""
    perf, created = TopicPerformance.objects.get_or_create(
        user=user,
        topic=topic,
        defaults={
            'total_attempts': 0,
            'avg_score': 0,
            'best_score': 0,
            'elo_points': 1000,
        }
    )

    perf.total_attempts += 1
    perf.best_score = max(perf.best_score, score)

    # Calculate running average
    perf.avg_score = (
        (perf.avg_score * (perf.total_attempts - 1) + score)
        / perf.total_attempts
    )

    # Calculate ELO gain based on score
    elo_change = _calculate_elo_change(score)
    perf.elo_points = max(100, perf.elo_points + elo_change)
    perf.last_attempt_at = timezone.now()
    
    # Update rank within topic
    perf.rank = _calculate_topic_rank(topic, perf.elo_points, user)
    
    perf.save()


def _calculate_elo_change(score: float) -> int:
    """
    Calculate ELO change based on score.
    Score 100% = +32 ELO, Score 0% = -16 ELO
    """
    elo_change = int((score / 100 * 48) - 16)
    # Minimum 1 point gain for any positive score
    if score > 0 and elo_change < 1:
        elo_change = 1
    return elo_change


def _calculate_topic_rank(topic: str, elo_points: int, current_user) -> int:
    """
    Calculate user's rank within a topic.
    Rank = number of users with higher ELO + 1
    """
    higher_count = TopicPerformance.objects.filter(
        topic=topic,
        elo_points__gt=elo_points
    ).exclude(user=current_user).count()
    
    return higher_count + 1


def get_topic_leaderboard(topic: str, limit: int = 10):
    """
    Get leaderboard for a specific topic.
    Similar to LeetCode problem set rankings.
    """
    return TopicPerformance.objects.filter(
        topic__iexact=topic
    ).select_related('user').order_by('-elo_points')[:limit]


def get_all_topics():
    """Get list of all topics with quiz counts."""
    from quizzes.models import Quiz
    return Quiz.objects.values_list('topic', flat=True).distinct()


def _calculate_rank(elo_points: int) -> str:
    """Calculate rank title based on ELO points."""
    if elo_points >= 2000:
        return "Master"
    elif elo_points >= 1800:
        return "Expert"
    elif elo_points >= 1600:
        return "Advanced"
    elif elo_points >= 1400:
        return "Intermediate"
    elif elo_points >= 1200:
        return "Beginner"
    else:
        return "Novice"


def _clear_performance_caches(topic: str = None):
    """Clear caches related to performance and leaderboards."""
    try:
        # Clear global leaderboard cache
        cache.delete('global_leaderboard')
        
        # Clear topic leaderboard cache
        if topic:
            cache.delete(f'topic_leaderboard_{topic.lower()}')
        
        # Clear topics cache (might have changed)
        cache.delete('all_topics')
    except:
        pass  # Cache might not be available
    
    # Clear user stats cache (if we had user-specific caching)