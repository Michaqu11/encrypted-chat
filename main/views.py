from django.shortcuts import render
from django.http import HttpResponse,  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config.ConfigFile import FIREBASE_CONFIG

import datetime
import pyrebase
import bcrypt
import rsa

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
authe = firebase.auth()
database = firebase.database()
save_key = None
ip = None

# Create your views here.

def index(response):
    return HttpResponse("<h1>S-CHAT</h1>")


@csrf_exempt
def login(request):
  data = database.child('Data').child('users').get().val()
  if request.POST.get('login') not in data:
    salt = bcrypt.gensalt()
    database.child('Data').child('users').push({
      "date": datetime.datetime.now(),
      "login": request.POST.get('login'),
      "password": bcrypt.hashpw(request.POST.get('password').encode('utf-8'), salt).decode('utf-8'),
    })
  
  result = {
    "error": False
  }

  return JsonResponse(result, safe=False)

@csrf_exempt
def generate_public_key(request):
  public_key, private_key = rsa.newkeys(1024 if request.POST.get('size') == "1024" else 2048)
  save_key = private_key

  result = {
    "public_key": '{0}'.format(public_key)
  }
  return JsonResponse(result, safe=False)


def chat(request):
  side = request.POST.get('chosedSide')
  ip = request.POST.get('ip')
