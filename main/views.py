from django.shortcuts import render
from django.http import HttpResponse,  JsonResponse
from django.views.decorators.csrf import csrf_exempt

import pyrebase
import bcrypt
import rsa

firebaseConfig = {
  "apiKey": "AIzaSyBp5y8j9lrwqZf1ptuU-35VFM1GIpLhPyw",
  "authDomain": "fir-chat-c3185.firebaseapp.com",
  "databaseURL": "https://fir-chat-c3185-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "fir-chat-c3185",
  "storageBucket": "fir-chat-c3185.appspot.com",
  "messagingSenderId": "822517477520",
  "appId": "1:822517477520:web:b79b724e4372958057e815"
}

firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database = firebase.database()

# Create your views here.

def index(response):
    return HttpResponse("<h1>S-CHAT</h1>")


@csrf_exempt
def login(request):
  data = database.child('Data').child('users').get().val()
  if request.POST.get('login') not in data:
    salt = bcrypt.gensalt()
    database.child('Data').child('users').push({
      "date": request.POST.get('date'),
      "login": request.POST.get('login'),
      "password": bcrypt.hashpw(request.POST.get('password').encode('utf-8'), salt).decode('utf-8'),
    })
  
  result = {
    "error": False
  }

  return JsonResponse(result, safe=False)

@csrf_exempt
def generate_public_key(request):
  public_key, private_key = rsa.newkeys(1024)

  result = {
    "public_key": '{0}'.format(public_key)
  }
  return JsonResponse(result, safe=False)
