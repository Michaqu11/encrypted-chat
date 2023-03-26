from django.urls import path, include

from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("public_key", views.generate_public_key, name="public_key")
]