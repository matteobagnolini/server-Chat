#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_connection():
    while True:
        client, client_address = SERVER.accept()    # client is the socket we use to communicate
        print("%s connected to chat" %client_address)
        client.send(bytes("Hello, what's your name?","utf8"))
        addresses[client] = client_address
        
        Thread(target = manage_client, args = (client)).start() # New thread for each connection

def manage_client(client):
    name = client.recv(BUFFSIZE).decode("utf8")
    clients[client] = name
    welcome = "Welcome to the chat, %s . Write {quit} to quit the chat" %name
    client.send(bytes(welcome, "utf8"))

    while True:
        msg = client.recv(BUFFSIZE).decode("utf8")
        if msg != "{quit}":
            formatted_msg = "[%s]: %s" %name %msg
            broadcast(bytes(formatted_msg, "utf8"))
        else:
            client.send(bytes("Goodbye!", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." %name, "utf8"))
            
def broadcast(msg): #TODO: add name prefix here instead of in manage_client
    for client in clients:
        client.send(bytes(msg, "utf8"))

clients = {}
addresses = {}

HOST = '127.0.0.1'
PORT = 5300
BUFFSIZE = 1024
ADDR = (HOST,PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(10)
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target = accept_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()