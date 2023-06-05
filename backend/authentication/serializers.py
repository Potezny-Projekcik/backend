from rest_framework import serializers
import sys

sys.path.append('..')
from authentication.auth import AccessTokenBackend


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    def create(self, validated_data):
        user = AccessTokenBackend().authenticate_username_password(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        if not user:
            raise serializers.ValidationError('Unable to log in with provided credentials.')

        return user

    def validate(self, data):
        user = self.create(data)
        print('user in validate')
        print(user)
        if not user.is_active:
            print("not active")
            raise serializers.ValidationError('User account is disabled.')

        data['user'] = user
        print(data)
        return data
