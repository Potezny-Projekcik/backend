from django.contrib import admin
from django.urls import path, include
from .views import CreateUserView, TestView

urlpatterns = [
    path('create-user/', CreateUserView.as_view(), name="create user"),
    path('test-post-request/', TestView.as_view(), name= "test api"),
]