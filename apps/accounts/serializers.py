from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
import re

User = get_user_model()

class RegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class ResetPasswordRequestSerializer(serializers.Serializer):
    """Serializer to validate the email for password reset request"""
    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if the email exists in the system"""
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer to validate and reset password"""
    password = serializers.CharField(
        write_only=True, 
        min_length=8,
        max_length=128,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        """Ensure passwords match"""
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        # Password strength check (optional)
        if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*#?&]{8,}$", password):
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long and contain at least one letter and one number."}
            )

        return data


class VerificationSerializer(serializers.Serializer):
    """Serializer to handle account verification"""
    token = serializers.CharField()

    def validate_token(self, value):
        """Check if token exists and is still valid"""
        user = User.objects.filter(verification_token=value).first()

        if not user:
            raise serializers.ValidationError("Invalid verification token.")

        if user.token_expires_at and timezone.now() > user.token_expires_at:
            raise serializers.ValidationError("Verification token has expired.")

        return value

