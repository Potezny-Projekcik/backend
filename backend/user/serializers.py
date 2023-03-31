from rest_framework import serializers
from .models import User
from .managers import CustomUserManager


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    login = serializers.CharField()
    birth_date = serializers.DateField()
    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'login', 'password', 'birth_date']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # def update(self, instance, validated_data):
    #     user = super().update(instance, validated_data)
    #     try:
    #         user.set_password(validated_data['password'])
    #         user.save()
    #     except KeyError:
    #         pass
    #     return user