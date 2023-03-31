from django.db import transaction
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User


class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)