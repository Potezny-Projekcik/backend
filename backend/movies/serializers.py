from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, Director, Directors, Language, Languages, Movie, Moviecategory, Producer, Producers, User, Usermovies

class CategorySerializer(serializers.ModelSerializer):
    categoryname = serializers.CharField(max_length=45)

    class Meta:
        model = Category
        fields = ('categoryid', 'categoryname')


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'


class DirectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Directors
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    languagename = serializers.CharField(max_length=45)

    class Meta:
        model = Language
        fields = ('languageid', 'languagename')


class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class MovieCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Moviecategory
        fields = '__all__'


class ProducerSerializer(serializers.ModelSerializer):
    producername = serializers.CharField(max_length=45)

    class Meta:
        model = Producer
        fields = ('producerid', 'producername')


class ProducersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producers
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    username = serializers.CharField()
    birthdate = serializers.DateField()
    isadmin = serializers.BooleanField()

    password = serializers.CharField(
        write_only=True,
        required=True,
        help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    class Meta:
        # model = User
        model = get_user_model()
        fields = "__all__"

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserMoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usermovies
        fields = '__all__'
