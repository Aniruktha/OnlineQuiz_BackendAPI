from django.urls import path
from .views import StartQuizView, SubmitAnswerView, SubmitQuizView

urlpatterns = [
    path("quiz/<int:quiz_id>/start/", StartQuizView.as_view()),
    path("attempt/<int:attempt_id>/answer/", SubmitAnswerView.as_view()),
    path("attempt/<int:attempt_id>/submit/", SubmitQuizView.as_view()),
]