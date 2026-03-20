"""
URL configuration for quiz_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.http import JsonResponse

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Root endpoint with API info
# API Documentation endpoint
@api_view(['GET'])
@renderer_classes([JSONRenderer, BrowsableAPIRenderer])
def api_docs(request):
    """API Documentation endpoint - returns browsable API with all endpoints."""
    return Response({
        "title": "Quiz API",
        "version": "v1",
        "description": "AI-Powered Quiz API with user management, quiz generation, and analytics",
        "endpoints": {
            "Authentication": {
                "register": {"url": "/api/users/register/", "method": "POST", "description": "Register new user"},
                "login": {"url": "/api/token/", "method": "POST", "description": "Get JWT tokens"},
                "refresh": {"url": "/api/token/refresh/", "method": "POST", "description": "Refresh access token"},
            },
            "Quizzes": {
                "list": {"url": "/api/quizzes/", "method": "GET", "description": "List all quizzes"},
                "create": {"url": "/api/quizzes/", "method": "POST", "description": "Create quiz (admin only)"},
                "questions": {"url": "/api/quizzes/{id}/questions/", "method": "GET", "description": "Get quiz questions"},
            },
            "Quiz Attempts": {
                "start": {"url": "/api/core/quiz/{id}/start/", "method": "POST", "description": "Start quiz attempt"},
                "answer": {"url": "/api/core/attempt/{id}/answer/", "method": "POST", "description": "Submit answer"},
                "submit": {"url": "/api/core/attempt/{id}/submit/", "method": "POST", "description": "Submit quiz"},
            },
            "Analytics": {
                "stats": {"url": "/api/analytics/stats/", "method": "GET", "description": "User statistics"},
                "leaderboard": {"url": "/api/analytics/leaderboard/", "method": "GET", "description": "Global leaderboard"},
                "topics": {"url": "/api/analytics/topics/", "method": "GET", "description": "List all topics"},
                "history": {"url": "/api/analytics/history/", "method": "GET", "description": "Quiz history"},
            }
        }
    })


def api_root(request):
    return JsonResponse({
        "message": "Welcome to Quiz API",
        "version": "v1",
        "endpoints": {
            "register": "/api/users/register/",
            "login": "/api/token/",
            "quizzes": "/api/quizzes/",
            "leaderboard": "/api/analytics/leaderboard/",
            "user_stats": "/api/analytics/stats/",
        },
        "docs": "/api/"
    })

urlpatterns = [
    path('', api_root, name='api_root'),
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/', api_docs, name='api_docs'),

    path("api/users/", include("users.urls")),
    path("api/quizzes/", include("quizzes.urls")),
    path("api/core/", include("core.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/ai/", include("ai.urls")),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
