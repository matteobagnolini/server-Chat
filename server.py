#!/usr/bin/env python3

from socket import AF_INET, socket, SOCK_STREAM
import sys
from threading import Thread
import time

# This method accepts connections from clients.
# It creates a new Thread for each client connected.
def accept_connection():
    while True:
        try:
            client, client_address = SERVER.accept()  # client is the socket we use to communicate
            print("%s:%s connected to chat" % client_address)
            client.send(bytes("Hello, what's your name?","utf8"))
            addresses[client] = client_address
        
            Thread(target = manage_client, args = (client,)).start() # New thread for each connection
        except OSError:
            print("Error in accepting new connections.")
            sys.exit()
        
# This method manages the client.
def manage_client(client):
    name = client.recv(BUFFSIZE).decode("utf8")
    if name in clients.values():     # If name already exists in chat
        name = create_unique_name(name)
        new_name_msg = "Your name was changed to %s, because the original one was already taken.\n" % name
        client.send(bytes(new_name_msg, "utf8"))
    clients[client] = name
    welcome = "Welcome to the chat, %s . Write {quit} to quit the chat" % name
    client.send(bytes(welcome, "utf8"))
    
    join_msg = "%s joined." % name
    print(join_msg)
    broadcast(join_msg)

    while True:     # Receiving messages from client
        try:
            msg = client.recv(BUFFSIZE).decode("utf8")
            if msg != "{quit}":
                curr_time = time.strftime("%H:%M", time.localtime())
                formatted_msg = "[%s] %s: %s" % (curr_time, name, msg)
                print(formatted_msg)
                broadcast(formatted_msg)
            else:
                client.send(bytes("Goodbye!", "utf8"))
                client.close()
                remove_client(client)
                break
        except OSError:
            print("Error while receiving messages from user %s." % clients[client])
            remove_client(client)
            break

# This method broadcasts a message to all the clients connected to the chat.
def broadcast(msg):
    for client in clients:
        try:
            client.send(bytes("%s" % msg, "utf8"))
        except OSError:
            print("Error while sending message to client.")
            remove_client(client)

# This method removes a client from the chat.
def remove_client(client):
    quit_msg = "%s has left the chat." % clients[client]
    del clients[client]
    print(quit_msg)
    broadcast(quit_msg)    

# This method is used to create an unique name.
# It should be used when a client choose a nickname which is already taken.
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

SERVER = socket(AF_INET, SOCK_STREAM)   # Server socket initialization
try:
    SERVER.bind(ADDR)
except OSError:
    print("Error while create a new bind with server.\nAborting..")
    sys.exit()

if __name__ == "__main__":
    SERVER.listen(10)
    print("Waiting for connections...")
    ACCEPT_THREAD = Thread(target = accept_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()