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
import hashlib
from base64 import b64encode, b64decode

firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
authe = firebase.auth()
database = firebase.database()




public_key = None
private_key = None
local_key = None

size = None
side = None
ip = None

login = None

# Create your views here.

def print_data():
    print(public_key, private_key, size, ip)


def index(request):
    return render(request, 'index.html', context={'text': 'S-CHAT'})
    # return HttpResponse("<h1>S-CHAT</h1>")

from cryptography.fernet import Fernet

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

@csrf_exempt
def login(request):
    data = database.child('Data').child('users').get().val()
    body = json.loads(request.body)
    global local_key, login

    if body['login'] not in data:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(body['password'].encode('utf-8'), salt).decode('utf-8')
        local_key = hashlib.sha256(password.encode()).digest()
        login  = database.child('Data').child('users').push(
        {
            "date": str(datetime.datetime.now()),
            "login": body['login'],
            "password": password
        })['name']

    else:
        login = data.child('Data').child('users').child(body['login']).get().val()
        

    # data = database.child('Data').child('users').get()

    # for d in data:
    #     if d.key() == login:
    #         print(d.val()['hash'])

    result = {
        "error": False
    }

    return JsonResponse(result, safe=False)


@csrf_exempt
def generate_public_key(request):
    global size, public_key, private_key
    size = 1024 if request.GET.get('size') == "1024" else 2048

    shahash = open("config/keys/hash.txt","r")
    hash = shahash.readline(0)
    shahash.close()

    if hash and hashlib.sha256(hash.encode()).hexdigest() == local_key:
        privFile = open("config/klocal_keyeys/priv.txt","r")
        pubFile = open("config/keys/pub.txt","r")
        private_key = Fernet(bytes(local_key)).decrypt(bytes(privFile.readline(0))).decode()
        public_key = pubFile.readline(0)
        pubFile.close()
        privFile.close()

    else:
        public_key, private_key = rsa.newkeys(size)
        privFile = open("config/keys/priv.txt","w")
        pubFile = open("config/keys/pub.txt","w")
        privFile.writelines(str(encrypt(private_key.save_pkcs1(), b64encode(local_key))))
        pubFile.writelines(str(public_key))
        pubFile.close()
        privFile.close()

    savehash = open("config/keys/hash.txt","w")
    savehash.writelines(str(local_key))
    savehash.close()


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
    if side == "host":
        hostname = socket.gethostname()
        temp_ip = socket.gethostbyname(hostname)
    else:
        temp_ip = body['ip']

    ip = temp_ip

    return JsonResponse({"ip": '{0}'.format(ip)}, safe=False)


@csrf_exempt
def start_connection(request):
    create_connection(side, ip, size, public_key, private_key)
    result = {
        "start-connection": True
    }

    return JsonResponse(result, safe=False)
