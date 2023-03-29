from django.shortcuts import render
from django.http import HttpResponse,  JsonResponse
from django.views.decorators.csrf import csrf_exempt
from config.ConfigFile import FIREBASE_CONFIG
from service.main import create_connection
import datetime
import pyrebase
import bcrypt
import rsa
import socket

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
authe = firebase.auth()
database = firebase.database()

public_key = None
private_key  = None
size = None
side = None
ip = None

# Create your views here.

def print_data():
  print(public_key, private_key, size, ip)


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
  global size, public_key, private_key
  size = 1024 if request.POST.get('size') == "1024" else 2048
  public_key, private_key = rsa.newkeys(size)
  result = {
    "public_key": '{0}'.format(public_key)
  }
  
  return JsonResponse(result, safe=False)

@csrf_exempt
def side(request):
  global side
  side = request.POST.get('chosedSide')
  global ip
  if side == "host":
    hostname = socket.gethostname()

    temp_ip = socket.gethostbyname(hostname)
  else:
    temp_ip  = request.POST.get('ip') 

  ip = temp_ip
  
  return JsonResponse({"ip" : '{0}'.format(ip)}, safe=False)
    
@csrf_exempt
def start_connection(request):
  create_connection(side, ip, size, public_key, private_key)

  result = {
    "start-connection": True
  }

  return JsonResponse(result, safe=False)
