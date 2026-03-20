from django.db import models
from users.models import CustomUser


class UserPerformance(models.Model):
    """Overall user performance across all topics."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True
    )

    total_attempts = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0)
    best_score = models.FloatField(default=0)

    elo_points = models.IntegerField(default=1000)
    rank = models.CharField(max_length=50, null=True, blank=True)

    last_attempt_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class TopicPerformance(models.Model):
    """User performance per topic - like LeetCode problem sets."""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='topic_performances'
    )
    
    topic = models.CharField(max_length=255)  # e.g., "Python", "JavaScript", "Data Structures"
    
    total_attempts = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0)
    best_score = models.FloatField(default=0)
    
    elo_points = models.IntegerField(default=1000)
    rank = models.IntegerField(default=0)  # Rank within this topic
    
    last_attempt_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['user', 'topic']
        indexes = [
            models.Index(fields=['topic', '-elo_points']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.topic}"