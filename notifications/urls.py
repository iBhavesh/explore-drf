from django.urls import path
from . import views

urlpatterns = [
    path('notifications', views.NotificationList.as_view(),
         name="notification-list"),
    path('notifications/read/<int:pk>',
         views.NotificationRead.as_view(), name='notification-read')
]
