import json

from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import render
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
private_key = None
size = None
side = None
ip = None
mode = "ECB"



# Create your views here.

def print_data():
    print(public_key, private_key, size, ip)


def index(request):
    return render(request, 'index.html', context={'text': 'S-CHAT'})
    # return HttpResponse("<h1>S-CHAT</h1>")


@csrf_exempt
def login(request):
    data = database.child('Data').child('users').get().val()
    body = json.loads(request.body)
    if body['login'] not in data:
        salt = bcrypt.gensalt()
        database.child('Data').child('users').push({
            "date": str(datetime.datetime.now()),
            "login": body['login'],
            "password": bcrypt.hashpw(body['password'].encode('utf-8'), salt).decode('utf-8'),
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
    body = json.loads(request.body)
    side = body['chosedSide']
    global ip
    global mode
    if side == "host":
        hostname = socket.gethostname()
        mode = body['encodingType']

        temp_ip = socket.gethostbyname(hostname)
    else:
        temp_ip = body['ip']

    ip = temp_ip

    return JsonResponse({"ip": '{0}'.format(ip)}, safe=False)


@csrf_exempt
def start_connection(request):
    create_connection(side, ip, size, public_key, private_key, mode)
    result = {
        "start-connection": True
    }

    return JsonResponse(result, safe=False)
