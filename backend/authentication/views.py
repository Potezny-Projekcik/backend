from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from django.http import JsonResponse
import requests
from django.contrib.auth import login, logout

import sys

from rest_framework.response import Response
from rest_framework import viewsets, permissions, serializers, status

sys.path.append('..')
from authentication.auth import AccessTokenBackend
from user.serializers import UserSerializer
from user.models import User

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:8000/api/authentication/dj-rest-auth/google/"
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):

        token_data = {
            'client_id': '82263305240-uv4nh847703q3n1978aqjcrka1o73k63.apps.googleusercontent.com',
            'client_secret': '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',
            'code': request.GET.get('code'),
            'grant_type': 'authorization_code',
            'redirect_uri': self.callback_url,
            'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/user.birthday.read',
        }

        token_response = requests.post('https://oauth2.googleapis.com/token', data=token_data)
        if token_response.status_code != 200:
            return Response({'error': 'Failed to obtain Google access token'}, status=400)

        google_token_data = token_response.json()
        access_token = google_token_data.get('access_token')
        refresh_token = google_token_data.get('refresh_token')


        if token_response.status_code == 200:
            # Extract the user data from the response
            user = AccessTokenBackend().authenticate(request, access_token=access_token)

            # If authentication is successful, log the user in and return a success response
            if user is not None:
                print(f'{request.user.is_authenticated} but before login')
                login(request, user)
                print(f'{request.user.is_authenticated} but after login')

                return Response({'success': True, 'access_token': access_token, 'refresh_token': refresh_token})
            else:
                return Response({'success': False, 'message': 'Invalid access token.'})

        return self.get_response()


from django.contrib.auth import get_user_model



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = AccessTokenBackend().authenticate_username_password(
            username=validated_data['username'],
            password=validated_data['password']
        )

        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        return user

    def validate(self, data):
        user = self.create(data)

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        data['user'] = user
        return data


class ModelLogin(viewsets.ModelViewSet):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def login(self, request):
        serializer = self.serializer_class(data=request.data, context=self.get_serializer_context())
        if serializer.is_valid():
            print(f'{request.user.is_authenticated} but before login')
            user = serializer.save()
            print("dupa")
            login(request, user)
            print(request.user.__dict__)
            print(f'{request.user.is_authenticated} but after login')
            return Response({'status': 'Authenticated'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def logout(self, request):
        print(request.user)
        print(request.user.is_authenticated)
        logout(request)
        print(request.user)
        print(request.user.is_authenticated)

        return Response({'status': 'Logged out',})





