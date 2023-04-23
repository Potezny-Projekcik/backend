from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView

from django.http import JsonResponse
import requests
from django.contrib.auth import  login


import sys
sys.path.append('..')
from authentication.auth import AccessTokenBackend


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
            return JsonResponse({'error': 'Failed to obtain Google access token'}, status=400)

        google_token_data = token_response.json()
        access_token = google_token_data.get('access_token')
        refresh_token = google_token_data.get('refresh_token')


        if token_response.status_code == 200:
            # Extract the user data from the response
            user = AccessTokenBackend().authenticate(request, access_token=access_token)

            # If authentication is successful, log the user in and return a success response
            if user is not None:
                login(request, user)
                print(request.user.is_authenticated)

                return JsonResponse({'success': True, 'access_token': access_token, 'refresh_token': refresh_token})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid access token.'})

        return self.get_response()

