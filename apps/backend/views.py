from rest_framework.decorators import api_view, permission_classes,parser_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.parsers import MultiPartParser
from django.apps import apps
from .models import User, UserProfile, QuizPool, QuizQuestion, QuizResult
from .serializers import UserProfileSerializer, QuizSerializer, QuestionSerializer, QuizResultSerializer
from apps.shared.serializers import SuccessResponseSerializer,ErrorResponseSerializer


# ----------------- USER PROFILE MANAGEMENT -----------------
@extend_schema(
    methods=["GET"],
    responses={200: UserProfileSerializer, 400: {"description": "Bad Request"}},
    summary="Retrieve User Profile",
    description="Retrieve the authenticated user's profile details.",
    tags=["User Profile"]
)
@extend_schema(
    methods=["PUT"],
    request=UserProfileSerializer,
    responses={200: UserProfileSerializer, 400: {"description": "Bad Request"}},
    summary="Update User Profile",
    description="Update the authenticated user's profile details.",
    tags=["User Profile"]
)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- QUIZ MANAGEMENT -----------------

@extend_schema(
    methods=["POST"],
    request=QuizSerializer,
    responses={201: QuizSerializer, 400: {"description": "Bad Request"}},
    summary="Create a Quiz",
    description="Allows authenticated users to create a new quiz.",
    tags=["Quiz Management"]
)
@extend_schema(
    methods=["GET"],
    responses={200: QuizSerializer(many=True), 400: {"description": "Bad Request"}},
    summary="Retrieve All Quizzes",
    description="Retrieves a list of all available quizzes created by authenticated user.",
    tags=["Quiz Management"]
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def quizzes(request):
    if request.method == 'GET':
        quizzes = QuizPool.objects.filter(user=request.user)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    methods=["DELETE"],
    parameters=[
        OpenApiParameter(
            name="quiz_id",
            type=int,
            location=OpenApiParameter.PATH,
            description="ID of the quiz to delete"
        )
    ],
    responses={
        200: {"description": "Quiz deleted successfully"},
        404: {"description": "Quiz not found"},
    },
    summary="Delete a Quiz",
    description="Deletes a quiz related to authenicated user",
    tags=["Quiz Management"]
)    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_quiz(request, quiz_id):
    quiz = QuizPool.objects.filter(id=quiz_id, user=request.user).first()

    if not quiz:
            return Response({"error": "Quiz not found or you are not authorized to delete it"}, status=status.HTTP_404_NOT_FOUND)

    quiz.delete()
    return Response({"message": "Quiz deleted successfully"}, status=status.HTTP_200_OK)

# ----------------- QUIZ QUESTIONS MANAGEMENT -----------------

@extend_schema(
    methods=["POST"],
    request=QuestionSerializer,
    responses={201: QuestionSerializer, 400: {"description": "Bad Request"}},
    summary="Add a Question to a Quiz",
    description="Allows authenticated users to add a question to a specific quiz.",
    tags=["Quiz Questions"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question(request, quiz_id):
    try:
        quiz = QuizPool.objects.get(id=quiz_id)
    except QuizPool.DoesNotExist:
        return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuestionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(quiz=quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ----------------- QUIZ RESULTS MANAGEMENT -----------------

@extend_schema(
    methods=["POST"],
    request=QuizResultSerializer,
    responses={201: QuizResultSerializer, 400: {"description": "Bad Request"}},
    summary="Submit Quiz Results",
    description="Submit quiz answers and calculate scores.",
    tags=["Quiz Results"]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request, quiz_id):
    try:
        quiz = QuizPool.objects.get(id=quiz_id)
    except QuizPool.DoesNotExist:
        return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = QuizResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(quiz=quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)