from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import authenticate, login
from .serializers import RegisterationSerializer, LoginSerializer,ResetPasswordSerializer,ResetPasswordRequestSerializer,VerificationSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenRefreshView
from django.utils import timezone
from django.contrib.auth import get_user_model
import requests  # For SMTP API
from django.conf import settings
from apps.shared.models import InternalServerError
from apps.shared.util import send_email

User = get_user_model()

#Register View
@extend_schema(
    request=RegisterationSerializer,
    responses={201: {"message": "User created successfully"}},
    summary="Registration",
    description="Endpoint for user registration.",
    tags=["SignIn/SignUp"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    try:
        serializer = RegisterationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Return a standardized internal server error response
        raise InternalServerError()

# Login View
@extend_schema(
    request=LoginSerializer,
    responses={
        200: {"message": "Logged in successfully"},
        401: {"error": "Invalid credentials"}
    },
    summary="Login",
    description="Endpoint for user signin.",
    tags=["SignIn/SignUp"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    try:
        # Validate request data using the serializer
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return Response({"message": "Logged in successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # Return validation errors if the request data is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            # Return a standardized internal server error response
            raise InternalServerError()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims if needed
        token['email'] = user.email
        return token

    def validate(self, attrs):
        # 'username' here expects the USERNAME_FIELD, so pass 'email' from request
        # if you want to rename it, you can override more extensively.
        return super().validate(attrs)


@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Obtain JWT Token",
        description="Endpoint to obtain a access token by providing valid credentials."
    )
)
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@extend_schema_view(
    post=extend_schema(
        tags=["Authentication"],
        summary="Refresh Jwt Token",
        description="Endpoint to refresh jwt token using a referesh token."
    )
)
class MyTokenRefreshView(TokenRefreshView):
    pass




# Send Verification Email
@extend_schema(
    request=None,
    responses={200: {"message": "Verification email sent"}},
    summary="Send Account Verification Email",
    description="Sends a verification email with an activation token.",
    tags=["Account Reset & Verification"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_verification_email_view(request):
    try:
        user = request.user

        if user.is_verified:
            return Response({"message": "User already verified"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.generate_verification_token()
        verification_link = f"{settings.PORTAL_WEB_APP_URL}/verify/{user.verification_token}"

        # Send email via SMTP API
        # Prepare email details
        subject = "Welcome to Rockea"
        body = f"Hi {user.username}, Welcome to Rockea. The team really loves you! Click the link below to verify your account:\n\n{verification_link}"
        recipients = [{
            "name": user.username,
            "email": user.email
        }]
        result = send_email(subject, body, recipients)

        return Response({"message": "Verification email sent."}, status=status.HTTP_200_OK)
    except Exception as e:
            # Return a standardized internal server error response
            raise InternalServerError(str(e))
    

# Verify Account View
@extend_schema(
    request=VerificationSerializer,
    responses={200: {"message": "Account verified successfully"}},
    summary="Verify Account",
    description="Verifies a user account using the verification token.",
    tags=["Account Reset & Verification"]
)
@api_view(['POST'])  # Change to POST to accept a JSON body
@permission_classes([AllowAny])
def verify_account_view(request):
    try:
        serializer = VerificationSerializer(data=request.data)
        
        if serializer.is_valid():
            token = serializer.validated_data.get("token")
            user = User.objects.filter(verification_token=token).first()

            user.is_verified = True
            user.verification_token = None
            user.token_expires_at = None
            user.save(update_fields=['is_verified', 'verification_token', 'token_expires_at'])

            return Response({"message": "Account verified successfully"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            # Return a standardized internal server error response
            raise InternalServerError()


# Password Reset Request View
@extend_schema(
    request=ResetPasswordRequestSerializer,
    responses={200: {"message": "Password reset email sent"}},
    summary="Request Password Reset",
    description="Sends a password reset email with a reset token.",
    tags=["Account Reset & Verification"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def send_password_reset_email_view(request):
    try:
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = User.objects.filter(email=email).first()
            
            if user:
                user.generate_reset_token()  # Generates a reset token
                reset_link = f"{settings.PORTAL_WEB_APP_URL}/reset-password/{user.reset_password_token}"

                # Send email via SMTP API
                email_data = {
                    "to": user.email,
                    "subject": "Reset Your Password",
                    "body": f"Click the link to reset your password: {reset_link}"
                }
                requests.post(settings.SMTP_SEND_MAIL_URL, json=email_data, headers={"Authorization": f"Bearer {settings.SMTP_API_KEY}"})

            return Response({"message": "Password reset email sent"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            # Return a standardized internal server error response
            raise InternalServerError()


# Reset Password View
@extend_schema(
    request=ResetPasswordSerializer,
    responses={200: {"message": "Password reset successful"}},
    summary="Reset Password",
    description="Allows users to reset their password using the reset token.",
    tags=["Account Reset & Verification"]
)
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_view(request, token):
    try:
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(reset_password_token=token).first()

            if user is None:
                return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.token_expires_at and timezone.now() > user.token_expires_at:
                return Response({"error": "Reset token expired"}, status=status.HTTP_400_BAD_REQUEST)

            # Update password
            user.set_password(serializer.validated_data.get('password'))
            user.reset_password_token = None
            user.token_expires_at = None
            user.save(update_fields=['password', 'reset_password_token', 'token_expires_at'])

            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
            # Return a standardized internal server error response
            raise InternalServerError()




