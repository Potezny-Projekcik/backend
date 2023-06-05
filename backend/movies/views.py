from rest_framework import viewsets
from .models import Category, Director, Directors, Language, Languages, Movie, Moviecategory, Producer, Producers, User, Usermovies
from .serializers import CategorySerializer, DirectorSerializer, DirectorsSerializer, LanguageSerializer, LanguagesSerializer, MovieSerializer, MovieCategorySerializer, ProducerSerializer, ProducersSerializer, UserSerializer, UserMoviesSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


class DirectorsViewSet(viewsets.ModelViewSet):
    queryset = Directors.objects.all()
    serializer_class = DirectorsSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer


class LanguagesViewSet(viewsets.ModelViewSet):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieCategoryViewSet(viewsets.ModelViewSet):
    queryset = Moviecategory.objects.all()
    serializer_class = MovieCategorySerializer


class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer


class ProducersViewSet(viewsets.ModelViewSet):
    queryset = Producers.objects.all()
    serializer_class = ProducersSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserMoviesViewSet(viewsets.ModelViewSet):
    queryset = Usermovies.objects.all()
    serializer_class = UserMoviesSerializer
