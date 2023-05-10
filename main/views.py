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
from cryptography.fernet import Fernet



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

def encrypt(message: bytes, key: bytes) -> bytes:
    return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
    return Fernet(key).decrypt(token)

@csrf_exempt
def login(request):
    data = database.child('Data').child('accounts').get()
    body = json.loads(request.body)
    global local_key, login

    logins = []

    for d in data:
        logins.append(d.val()['login'])

    if body['login'] not in logins:
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw(body['password'].encode('utf-8'), salt).decode('utf-8')
        local_key = hashlib.sha256(password.encode()).digest()
        login  = database.child('Data').child('accounts').push(
        {
            "date": str(datetime.datetime.now()),
            "login": body['login'],
            "password": password
        })['name']

    else:
        for d in data:
            if d.val()['login'] == body['login']:
                local_key = hashlib.sha256(d.val()['password'].encode()).digest()

    result = {
        "error": False
    }

    return JsonResponse(result, safe=False)


@csrf_exempt
def generate_public_key(request):
    global size, public_key, private_key
    size = 1024 if request.GET.get('size') == "1024" else 2048

    shahash = open("config/keys/hash.txt","rb")
    hash = shahash.read()
    shahash.close()

    if hash and local_key == hash:
        privFile = open("config/keys/priv.txt","rb")
        pubFile = open("config/keys/pub.txt","rb")
        token = privFile.read()
        public_key = rsa.PublicKey.load_pkcs1(pubFile.read())
        private_key = rsa.PrivateKey.load_pkcs1(decrypt(token, b64encode(local_key)))
        pubFile.close()
        privFile.close()

    else:
        public_key, private_key = rsa.newkeys(size)
        privFile = open("config/keys/priv.txt","wb")
        pubFile = open("config/keys/pub.txt","wb")
        token = encrypt(private_key.save_pkcs1("PEM"), b64encode(local_key))
        privFile.write(token)
        pubFile.write(public_key.save_pkcs1("PEM"))
        pubFile.close()
        privFile.close()

    savehash = open("config/keys/hash.txt","wb")
    savehash.write(local_key)
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
