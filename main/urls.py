from django.urls import path, include

from . import views 

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("key", views.generate_public_key, name="key"),
    path("chat", views.chat, name="chat")
]