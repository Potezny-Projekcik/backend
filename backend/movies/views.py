from rest_framework import viewsets
from .models import Category, Director, Directors, Language, Languages, Movie, Moviecategory, Producer, Producers, User, Usermovies
from .serializers import CategorySerializer, DirectorSerializer, DirectorsSerializer, LanguageSerializer, LanguagesSerializer, MovieSerializer, MovieCategorySerializer, ProducerSerializer, ProducersSerializer, UserSerializer, UserMoviesSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import connection
import psycopg2


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
    @action(detail=False, methods=['get'], url_path='get-movies-by-category/(?P<category_id>[^/.]+)')
    def get_usermovies_by_category(self, request, category_id):
        query = """
            SELECT DISTINCT ON ("UserMovies".usermovieid)
            "UserMovies".*, "Movie".title, "Movie".genre, "Movie".countryoforigin, "Movie".productionyear, "Movie".suggestedage,
            "Producer".producername, "Director".directorfirstname, "Director".directorlastname, "Language".languagename
            FROM "UserMovies"
            INNER JOIN "MovieCategory" ON "UserMovies".usermovieid = "MovieCategory".usermovieid
            INNER JOIN "Movie" ON "UserMovies".movieid = "Movie".movieid
            LEFT JOIN "Producers" ON "UserMovies".movieid = "Producers".movieid
            LEFT JOIN "Producer" ON "Producers".producerid = "Producer".producerid
            LEFT JOIN "Directors" ON "UserMovies".movieid = "Directors".movieid
            LEFT JOIN "Director" ON "Directors".directorid = "Director".directorid
            LEFT JOIN "Languages" ON "UserMovies".movieid = "Languages".movieid
            LEFT JOIN "Language" ON "Languages".languageid = "Language".languageid
            WHERE  "MovieCategory".categoryid=
        """
        secondQuery=f"{query}{category_id}"
        print(secondQuery)

        # Execute the raw query
        with connection.cursor() as cursor:
            cursor.execute(secondQuery)
            results = cursor.fetchall()

        return Response(results)