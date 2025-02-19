from rest_framework import serializers
from .models import UserProfile,QuizPool,QuizQuestion,QuizResult

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizPool
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = '__all__'

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = '__all__'