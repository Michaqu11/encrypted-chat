import sys
import socket
import threading

import rsa

def sending_messages(c, public_partner):
    while True:
        message = input("")
        c.send(rsa.encrypt(message.encode(), public_partner))
        print("You: " + message)


def reveiving_message(c, private_key):
    while True:
        print("Partner: " + rsa.decrypt(c.recv(1024), private_key).decode())

def create_connection(choice):

    hostname = socket.gethostname()git restore
    IPAddr = socket.gethostbyname(hostname)

    public_key, private_key = rsa.newkeys(1024)
    public_partner = None

    if choice == "1":  # host
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IPAddr, 9999))
        server.listen()

        client, _ = server.accept()
        client.send(public_key.save_pkcs1("PEM"))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

    elif choice == "2":
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IPAddr, 9999))
        public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))
        client.send(public_key.save_pkcs1("PEM"))

    else:
        exit()

    threading.Thread(target=sending_messages, args=(client,public_partner)).start()
    threading.Thread(target=reveiving_message, args=(client, private_key)).start()



create_connection(sys.argv[1])