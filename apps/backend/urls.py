from django.urls import path
from .views import user_profile, quizzes, add_question, submit_quiz,delete_quiz

urlpatterns = [
    path('user/profile/', user_profile, name="user-profile"),
    path('quiz/', quizzes, name="quizzes"),
    path('quiz/<int:quiz_id>/', delete_quiz, name="delete-quiz"),
    path('quiz/<int:quiz_id>/question/', add_question, name="add-question"),
    path('quiz/<int:quiz_id>/submit/', submit_quiz, name="submit-quiz"),
]
