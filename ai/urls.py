from django.urls import path
from .views import WeakTopicAnalysisView

urlpatterns = [
    path("analysis/", WeakTopicAnalysisView.as_view()),
]