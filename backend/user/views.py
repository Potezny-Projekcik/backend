from django.db import transaction
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from django.db import connection

# Your code that interacts with the database




class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]
    # permission_classes = [permissions.IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)


class TestView(APIView):
    # permission_classes = [permissions.AllowAny]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request.data)
        return Response(request.data)

    def get(self, request):
        print(request.user)
        print(request.user.__dict__)
        return Response("Hello authenticated user")