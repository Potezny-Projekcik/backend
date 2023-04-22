from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView, LoginView

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.google.views import OAuth2Error
from google_auth_oauthlib.flow import Flow
from rest_framework import permissions, status

from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
import requests
from dj_rest_auth.serializers import LoginSerializer

from rest_framework.views import APIView
# import chardet

import jwt
import sys

sys.path.append('..')
from user.models import User


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def complete_login(self, request, app, token, response, **kwargs):
        try:
            identity_data = jwt.decode(
                response["id_token"]["id_token"],  # another nested id_token was returned
                options={
                    "verify_signature": False,
                    "verify_iss": True,
                    "verify_aud": True,
                    "verify_exp": True,
                },
                issuer=self.id_token_issuer,
                audience=app.client_id,
            )
        except jwt.PyJWTError as e:
            raise OAuth2Error("Invalid id_token") from e
        login = self.get_provider().sociallogin_from_response(request, identity_data)
        return login


class GoogleLogin(SocialLoginView):
    adapter_class = CustomGoogleOAuth2Adapter
    callback_url = "http://localhost:8000/api/authentication/dj-rest-auth/google/"
    client_class = OAuth2Client

    def get(self, request, *args, **kwargs):
        print(request.GET.get('code'))
        self.request = request
        self.serializer = self.get_serializer(data=self.request.GET)
        self.serializer.is_valid(raise_exception=True)

        self.login()
        print(self.get_response().data['access_token'])
        return self.get_response()



