import requests
from django.contrib.auth.backends import BaseBackend

import sys
sys.path.append('..')
# from backend.models import User
from movies.models import User

class AccessTokenBackend(BaseBackend):
    def authenticate_google_provider(self, request, access_token=None):

        if access_token is None:
            return None

        provider_url = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,birthdays'

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(provider_url, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            try:
                username=user_data['names'][0]['displayName'][:32]
                user = User.objects.get(username=username)
                user.backend = 'authentication.auth.AccessTokenBackend'

            except User.DoesNotExist:
                if 'birthdays' in user_data:
                    for birthday in user_data['birthdays']:
                        if 'date' in birthday and 'year' in birthday['date']:
                            date = birthday['date']
                            user_birthday = f"{date['year']}-{date['month']}-{date['day']}"

                print(user_data['names'][0]['displayName'])
                username=user_data['names'][0]['displayName'].replace(' ', '')[:32]
                user = User.objects.create_user(
                    username=username,
                    firstname=user_data['names'][0]['givenName'],
                    lastname=user_data['names'][0]['familyName'],
                    birthdate=user_birthday
                )

            if user is not None:
                return user
        return None


    def authenticate_username_password(self, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            user.backend = 'authentication.auth.AccessTokenBackend'
            return user

        return None

    def authenticate_header(self, request):
        return 'Bearer realm="api", charset="UTF-8"'