from django.urls import path, re_path
from .views import GoogleLogin

urlpatterns = [
    re_path(r"^dj-rest-auth/google/$", GoogleLogin.as_view(), name="google_login"),
]
