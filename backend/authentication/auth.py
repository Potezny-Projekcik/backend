import requests
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend

import sys

from django.contrib.auth.hashers import check_password

sys.path.append('..')
# from backend.models import User
from movies.models import User
import hashlib
from django.contrib.auth.hashers import make_password, check_password




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
        if username is None or password is None:
            print("Username or password not provided")
            return None

        hashed_password_from_db = "pbkdf2_sha256$390000$LECMuaeRd6UIhxCMhqMuSi$DX0iib26Pry4ruLOKCxKsALAIpX7FOnWSNn/UGl+gmg="
        provided_password = "kek"

        # Hash the provided password with the same method, salt and iterations
        hashed_provided_password = make_password(provided_password, salt='LECMuaeRd6UIhxCMhqMuSi',
                                                 hasher='pbkdf2_sha256')

        print("Hashed provided password:", hashed_provided_password)

        # Compare the two hashed passwords
        print("Passwords match:", hashed_password_from_db == hashed_provided_password)

        # Or use check_password
        print("check_password result:", check_password(provided_password, hashed_password_from_db))


        try:
            print("In authenticate")
            user = User.objects.get(username=username)
            print(f"User: {user}")

        except User.DoesNotExist:
            print("User does not exist")
            return None

        print("check_password result:", check_password(password.replace(" ", ""), user.password.replace(" ", "")))


        user.backend = 'django.contrib.auth.backends.ModelBackend'

        if check_password(password.replace(" ", ""), user.password.replace(" ", "")):
            print("Password is correct")
            return user
        else:
            print(f"Password is incorrect. Hashed password: {user.password}, provided password: {password}")
            return None

    # def authenticate_username_password(self, username=None, password=None):
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         return None
    #
    #     if check_password(password, user.password):
    #         user.backend = 'authentication.auth.AccessTokenBackend'
    #         return user
    #
    #     return None


    def authenticate_header(self, request):
        return 'Bearer realm="api", charset="UTF-8"'