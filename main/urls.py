from django.urls import path, include

from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("key", views.generate_public_key, name="key"),
    path("side", views.side, name="side"),
    path("start_connection", views.start_connection, name="start_connection")
]