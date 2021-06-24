from django.urls import path
from . import views
urlpatterns = [
    path("<int:pk>", views.get_followers, name="get-followers")
]
