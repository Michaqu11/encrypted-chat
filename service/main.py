import socket
import threading

import rsa
from random import randrange
import sys

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import threading

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

sys.path.insert(0, '..')

channel_layer = get_channel_layer()
messagesToSend = []
session_key = None
condition_object = threading.Condition()


def pushToMessages(message):
    condition_object.acquire()
    messagesToSend.insert(0, message)
    condition_object.notify()
    condition_object.release()
    
def sending_messages(c, public_partner, cipher):

    while True:
        if(len(messagesToSend)):
            data = messagesToSend.pop()
            # c.send(cipher.encrypt(data['message'].encode()))
            c.send(rsa.encrypt(data['message'].encode(), public_partner))
            print("You: " + data['message'])
        else:
            condition_object.acquire()
            condition_object.wait()
            condition_object.release()
    

def reveiving_message(c, private_key, size, decipher):
    while True:
        message = rsa.decrypt(c.recv(size), private_key).decode()
        # message = decipher.decrypt(c.recv(size)).decode()
        print("Partner: " + message)
        async_to_sync(channel_layer.group_send)(
            'chat',
            {
                "type": "chat.message",
                'message': message,
                'from': "recv"
            }
        )


def create_connection(side, IPAddr, size, public_key, private_key, mode):
    public_partner = None
    global session_key
    if side == "host":  # host
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IPAddr, 9999))
        server.listen()

        client, _ = server.accept()
        client.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(size))
        
        session_key = get_random_bytes(16)
        client.send(rsa.encrypt(session_key, public_partner)) # session key
        client.send(rsa.encrypt(mode.encode(), public_partner)) # AES mode


    elif side == "client":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IPAddr, 9999))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(size))
        client.send(public_key.save_pkcs1("PEM"))
        session_key = rsa.decrypt(client.recv(size), private_key)
        mode = rsa.decrypt(client.recv(size), private_key).decode()

    else:
        exit(0)

    cipher = AES.new(session_key,  AES.MODE_ECB if mode == "ECB" else AES.MODE_CBC)

    threading.Thread(target=sending_messages, args=(client,public_partner, cipher)).start()
    threading.Thread(target=reveiving_message, args=(client, private_key, size, cipher)).start()

