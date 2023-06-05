"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
# from .views import (
#     CategoryViewSet, DirectorViewSet, DirectorsViewSet,
#     LanguageViewSet, LanguagesViewSet, MovieViewSet,
#     MovieCategoryViewSet, ProducerViewSet, ProducersViewSet,
#     UserViewSet, UserMoviesViewSet
# )

# router = routers.DefaultRouter()
# router.register('category', CategoryViewSet)
# router.register('director', DirectorViewSet)
# router.register('directors', DirectorsViewSet)
# router.register('language', LanguageViewSet)
# router.register('languages', LanguagesViewSet)
# router.register('movie', MovieViewSet)
# router.register('moviecategory', MovieCategoryViewSet)
# router.register('producer', ProducerViewSet)
# router.register('producers', ProducersViewSet)
# router.register('user', UserViewSet)
# router.register('usermovies', UserMoviesViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('user/', include('user.urls')),
    path('authentication/', include('authentication.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    path('jwt/', include('JWT_Tokens.urls')),
    # path('', include(router.urls)),
    path('', include('movies.urls')),

]

urlpatterns = [path('api/', include(urlpatterns))]


# https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fapi%2Fauthentication%2Fdj-rest-auth%2Fgoogle%2F&prompt=consent&response_type=code&client_id=82263305240-uv4nh847703q3n1978aqjcrka1o73k63.apps.googleusercontent.com&scope=openid%20email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuser.birthday.read&access_type=offline&service=lso&o2v=2&flowName=GeneralOAuthFlow