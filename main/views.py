from django.shortcuts import render
from django.http import HttpResponse

# import socket
# import threading


# Create your views here.

def index(response):
    return HttpResponse("<h1>S-CHAT</h1>")