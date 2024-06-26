#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time

def accept_connection():
    while True:
        client, client_address = SERVER.accept()  # client is the socket we use to communicate
        print("%s:%s connected to chat" % client_address)
        client.send(bytes("Hello, what's your name?","utf8"))
        addresses[client] = client_address
        
        Thread(target = manage_client, args = (client,)).start() # New thread for each connection

def manage_client(client):
    name = client.recv(BUFFSIZE).decode("utf8")
    if name in clients.values():     # If name already exists in chat
        name = create_unique_name(name)
        new_name_msg = "Your name was changed to %s, because the original one was already taken.\n" % name
        client.send(bytes(new_name_msg, "utf8"))
    clients[client] = name
    welcome = "Welcome to the chat, %s . Write {quit} to quit the chat" % name
    client.send(bytes(welcome, "utf8"))
    
    print(name, " joined.")

    while True:
        msg = client.recv(BUFFSIZE).decode("utf8")
        if msg != "{quit}":
            curr_time = time.strftime("%H:%M", time.localtime())
            formatted_msg = "[%s] %s: %s" % (curr_time, name, msg)
            print(formatted_msg)
            broadcast(formatted_msg)
        else:
            client.send(bytes("Goodbye!", "utf8"))
            client.close()
            del clients[client]
            quit_msg = "%s has left the chat." % name
            broadcast(quit_msg)
            print(quit_msg)
            break
            
def broadcast(msg):
    for client in clients:
        client.send(bytes("%s" % msg, "utf8"))

def create_unique_name(name):
    original_name = name
    count = 1
    
    while name in clients.values():
        name = f"{original_name}_{count}"
        count += 1
    return name

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