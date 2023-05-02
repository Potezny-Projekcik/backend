from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
import requests
from django.contrib.auth import login, logout
from rest_framework.views import APIView

import sys

from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from .serializers import LoginSerializer
sys.path.append('..')
from authentication.auth import AccessTokenBackend
from JWT_Tokens.JWT import create_jwt_pair_for_user, delete_token

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

        if token_response.status_code == 200:
            user = AccessTokenBackend().authenticate_google_provider(request, access_token=access_token)

            if user is not None:
                login(request, user)
                return Response(create_jwt_pair_for_user(user))
            else:
                return Response({'success': False, 'message': 'Invalid access token.'})

        return self.get_response()


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
            tokens = create_jwt_pair_for_user(user)
            login(request, user)
            print(request.user.__dict__)
            print(f'{request.user.is_authenticated} but after login')
            return Response(tokens)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):

    def get(self, request):
        # change logout method to post and username from jwt token
        logout(request)
        # user = User.objects.get(id=request.user.id)
        # delete_token(user)
        return Response({'status': 'Logged out',})




