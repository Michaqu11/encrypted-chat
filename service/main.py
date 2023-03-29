import sys
import socket
import threading

import rsa
import time
from random import randrange

def sending_messages(c, public_partner):
    while True:
        nr = randrange(100000)
        message = 'test ({0})'.format(nr) 
        time.sleep(5+randrange(5))
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)


def reveiving_message(c, private_key, size):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(size), private_key).decode())

def create_connection(side, IPAddr, size, public_key, private_key):

    public_partner = None 
    
    if side == "host":  # host
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IPAddr, 9999))
        server.listen()

        client, _ = server.accept()
        client.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(size))

    elif side == "client":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IPAddr, 9999))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(size))
        client.send(public_key.save_pkcs1("PEM"))

    else:
        exit(0)

    threading.Thread(target=sending_messages, args=(client,public_partner)).start()
    threading.Thread(target=reveiving_message, args=(client, private_key, size)).start()

