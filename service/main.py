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
from Crypto import Random
from base64 import b64encode, b64decode

from time import sleep
from random import randrange
import json

sys.path.insert(0, '..')

channel_layer = get_channel_layer()
messagesToSend = []
session_key = None
condition_object = threading.Condition()
block_size = AES.block_size
conifg = 1/100000


def pad(plain_text):
    number_of_bytes_to_pad = block_size - len(plain_text) % block_size
    ascii_string = chr(number_of_bytes_to_pad)
    padding_str = number_of_bytes_to_pad * ascii_string
    padded_plain_text = plain_text + padding_str
    return padded_plain_text

def unpad(plain_text):
    last_character = plain_text[len(plain_text) - 1:]
    bytes_to_remove = ord(last_character)
    return plain_text[:-bytes_to_remove]

def pushToMessages(message):
    condition_object.acquire()
    messagesToSend.insert(0, message)
    condition_object.notify()
    condition_object.release()


def sending_messages(c, public_partner):

    while True:
        if(len(messagesToSend)):
            data = messagesToSend.pop()
            plain_text = pad(data['message'])
            mode = data['mode']
           
            if mode == "CBC":
                iv = Random.new().read(block_size)
                cipher = AES.new(session_key, AES.MODE_CBC, iv)
                encrypted_text = cipher.encrypt(plain_text.encode())

                json_data = json.dumps({"encrypted_text": b64encode(iv + encrypted_text).decode(), "type":  data['type'], "mode": mode})

            else:
                cipher = AES.new(session_key, AES.MODE_ECB)
                encrypted_text = cipher.encrypt(plain_text.encode())
                json_data = json.dumps({"encrypted_text":b64encode(encrypted_text).decode(), "type":  data['type'], "mode": mode})

            if  data['type'] == "text":   
                c.send(bytes(json_data, 'utf-8'))
                print("You: " + data['message'])
            
            else: #file
                size = 256
                max_size = int(len(encrypted_text) / size)

                if mode == "CBC":
                    json_data = json.dumps({"type":  data['type'], "iv": b64encode(iv).decode(), "mode": mode, "max_size": max_size})
                else:
                    json_data = json.dumps({"type":  data['type'], "mode": mode,  "max_size": max_size})

                c.send(bytes(json_data, 'utf-8'))

                if max_size:
                    for i in range(0, len(encrypted_text), size):
                        chunk = encrypted_text[i:i + size]
                        sleep(conifg)
                        c.send(b64encode(chunk))
                else:
                    c.send(b64encode(encrypted_text))
                
                print("You: " + "file")
                    
        else:
            condition_object.acquire()
            condition_object.wait()
            condition_object.release()
    

def reveiving_message(c, private_key, size):
    while True:
        json_data = json.loads(c.recv(size).decode("utf-8"))
        mode = json_data['mode']
        type = json_data['type']

        if type == "text":
            if mode == "CBC":
                encrypted_text = b64decode(json_data['encrypted_text'])
                iv = encrypted_text[:block_size]
                cipher = AES.new(session_key, AES.MODE_CBC, iv)
                plain_text = cipher.decrypt(encrypted_text[block_size:]).decode()
                message = unpad(plain_text)
            else:
                encrypted_text = b64decode(json_data['encrypted_text'])
                cipher = AES.new(session_key, AES.MODE_ECB)
                plain_text = cipher.decrypt(encrypted_text).decode()
                message = unpad(plain_text)
            print("Partner: " + message)

        else:
            message = b""

            if mode == "CBC":
                iv = b64decode(json_data['iv'])
                cipher = AES.new(session_key, AES.MODE_CBC, iv)
              
            else:
                cipher = AES.new(session_key, AES.MODE_ECB)

            max_size = json_data['max_size']

            if max_size:
                for i in range(0, max_size + 1):
                    data = c.recv(size).decode("utf-8")
                    message = message + b64decode(data)
            else:
                data = c.recv(size).decode("utf-8")
                message = b64decode(data)

            plain_text = cipher.decrypt(message).decode()
            result = unpad(plain_text)

            print("Partner: " + "file")

    

        async_to_sync(channel_layer.group_send)(
            'chat',
            {
                "type": "chat.message",
                'message': result,
                'from': "recv"
            }
        )


def create_connection(side, IPAddr, size, public_key, private_key):
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


    elif side == "client":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IPAddr, 9999))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(size))
        client.send(public_key.save_pkcs1("PEM"))
        session_key = rsa.decrypt(client.recv(size), private_key)

    else:
        exit(0)

    threading.Thread(target=sending_messages, args=(client,public_partner)).start()
    threading.Thread(target=reveiving_message, args=(client, private_key, size)).start()

