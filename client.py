from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tkt

# Method to receive message from the chat
def receive():
    while True:
        try:
        
            msg = client_socket.recv(BUFFSIZE).decode("utf8")
            msg_list.insert(tkt.END, msg)
        
        except OSError:
            break

# Method to send message to the chat
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        window.quit()

# Action to perform when the window is closed
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

# Window initialization
window = tkt.Tk()
window.title("Chat")

message_frame = tkt.Frame(window)

# Text field
my_msg = tkt.StringVar()
my_msg.set("Insert here your text")
scrollbar = tkt.Scrollbar(message_frame)

# Messages box
msg_list = tkt.Listbox(message_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
msg_list.pack()
message_frame.pack()

# Input field
entry_field = tkt.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()

# Send button
send_button = tkt.Button(window, text="Send", command=send)
send_button.pack()

# When closing window
window.protocol("WM_DELETE_WINDOW", on_closing)

#HOST = input("Server host: ")
#PORT = input("Server port: ")
HOST = "127.0.0.1"
PORT = 5300


if not PORT:        # Invalid port
    PORT = 5300
else:
    PORT = int(PORT)

BUFFSIZE = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target = receive)
receive_thread.start()

tkt.mainloop()