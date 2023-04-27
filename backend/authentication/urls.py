from django.urls import path, re_path
from .views import GoogleLogin, ModelLogin

urlpatterns = [
    re_path(r"^dj-rest-auth/google/$", GoogleLogin.as_view(), name="google_login"),
    path('model-login', ModelLogin.as_view({'post': 'login', 'get': 'logout'}), name='basic-login')
]
