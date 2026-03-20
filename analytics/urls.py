from django.urls import path
from .views import (
    UserStatsView, 
    LeaderboardView, 
    QuizHistoryView,
    TopicLeaderboardView,
    TopicsListView
)

urlpatterns = [
    path("stats/", UserStatsView.as_view()),
    path("leaderboard/", LeaderboardView.as_view()),  # Global leaderboard
    path("leaderboard/<str:topic>/", TopicLeaderboardView.as_view()),  # Topic leaderboard
    path("topics/", TopicsListView.as_view()),  # List all topics
    path("history/", QuizHistoryView.as_view()),
]