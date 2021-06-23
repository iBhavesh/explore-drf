from django.urls import path
from . import views

urlpatterns = [
    path('test-auth', views.TestView.as_view()),
    path('image/upload', views.uploadImage),
]
