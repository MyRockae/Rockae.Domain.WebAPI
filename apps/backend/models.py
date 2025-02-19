from django.db import models
from apps.accounts.models import User  # adjust path if needed

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.lastname
    
    class Meta:
        db_table = 'UserProfile'
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfile'
        

class QuizPool(models.Model):
    quiz_title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    candidate_auth_required = models.BooleanField(default=True)

    def __str__(self):
        return self.quiz_title
    
    class Meta:
        db_table = 'QuizPool'
        verbose_name = 'QuizPool'
        verbose_name_plural = 'QuizPool'


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(QuizPool, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    answer_a = models.CharField(max_length=255)
    answer_b = models.CharField(max_length=255)
    answer_c = models.CharField(max_length=255)
    answer_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"Quiz: {self.quiz.quiz_title} | Question: {self.question_text[:50]}"
    
    class Meta:
        db_table = 'QuizQuestion'
        verbose_name = 'QuizQuestion'
        verbose_name_plural = 'QuizQuestions'

class QuizResult(models.Model):
    quiz = models.ForeignKey(QuizPool, on_delete=models.CASCADE)
    candidate_name = models.CharField(max_length=255)
    candidate_app_id = models.CharField(max_length=255, null=True, blank=True)
    completion_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()

    def __str__(self):
        return f"Result for {self.candidate_name} - {self.score}%"
    
    class Meta:
        db_table = 'QuizResult'
        verbose_name = 'QuizResult'
        verbose_name_plural = 'QuizResults'