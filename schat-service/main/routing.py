from django.urls import path

from .consumers import WSConsumer

instance = WSConsumer.as_asgi()


ws_urlpatterns = [
    path('ws/socket-server/', instance)
]