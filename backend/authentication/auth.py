import requests
from django.contrib.auth.backends import BaseBackend

import sys
sys.path.append('..')
from user.models import User

class AccessTokenBackend(BaseBackend):
    def authenticate(self, request, access_token=None):

        if access_token is None:
            return None

        # Send a request to the provider's API to verify the access token
        provider_url = 'https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,birthdays'

        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(provider_url, headers=headers)

        # Check if the response contains user information
        if response.status_code == 200:
            user_data = response.json()
            print('in authenticate')
            print(user_data)
            # Check if the user exists in the database
            try:
                user = User.objects.get(username=user_data['names'][0]['displayName'])
                user.backend = 'authentication.auth.AccessTokenBackend'

            except User.DoesNotExist:

                if 'birthdays' in user_data:
                    for birthday in user_data['birthdays']:
                        if 'date' in birthday and 'year' in birthday['date']:
                            date = birthday['date']
                            user_birthday = f"{date['year']}-{date['month']}-{date['day']}"

                user = User.objects.create_user(
                    username=user_data['names'][0]['displayName'],
                    first_name=user_data['names'][0]['givenName'],
                    last_name=user_data['names'][0]['familyName'],
                    birth_date=user_birthday
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