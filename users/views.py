from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(APIView):

    permission_classes = []

    def post(self, request):
        # Check if user already exists before validation
        username = request.data.get("username")
        email = request.data.get("email")
        
        # Check if user already exists
        existing_user = None
        was_existing = False
        
        if User.objects.filter(username=username).exists():
            existing_user = User.objects.get(username=username)
            was_existing = True
        elif User.objects.filter(email=email).exists():
            existing_user = User.objects.get(email=email)
            was_existing = True
        
        # If user exists, return their info without creating
        if was_existing and existing_user:
            return Response({
                "message": "User already exists",
                "username": existing_user.username,
                "email": existing_user.email,
                "is_admin": existing_user.is_staff,
                "is_staff": existing_user.is_staff,
                "status": "existing"
            }, status=status.HTTP_200_OK)
        
        # Create new user
        serializer = RegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = serializer.save()

        return Response({
            "message": "User created successfully",
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_staff,
            "is_staff": user.is_staff,
            "status": "created"
        }, status=status.HTTP_201_CREATED)