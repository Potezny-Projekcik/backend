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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('user/', include('user.urls')),
    path('authentication/', include('authentication.urls')),
    path('auth/', include('dj_rest_auth.urls')),

]

urlpatterns = [path('api/', include(urlpatterns))]


# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://localhost:8000/api/authentication/dj-rest-auth/google/&prompt=consent&response_type=code&client_id=82263305240-uv4nh847703q3n1978aqjcrka1o73k63.apps.googleusercontent.com&scope=openid%20email%20profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuser.birthday.read&access_type=offline
# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://localhost:8000/api/authentication/google/callback/&prompt=consent&response_type=code&client_id=82263305240-uv4nh847703q3n1978aqjcrka1o73k63.apps.googleusercontent.com&scope=openid%20email%20profile&access_type=offline