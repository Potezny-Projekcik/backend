from django.urls import path, re_path
from .views import GoogleLogin, ModelLogin, LogoutUser

urlpatterns = [
    re_path(r"^dj-rest-auth/google/$", GoogleLogin.as_view(), name="google_login"),
    path('model-login/', ModelLogin.as_view({'post': 'login'}), name='model-login'),
    path('logout/', LogoutUser.as_view(), name='logout')
]
