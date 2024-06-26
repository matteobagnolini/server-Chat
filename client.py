from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import tkinter as tkt

# Method to receive messages from server.
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFFSIZE).decode("utf8")
            print(msg)
            msg_list.insert(tkt.END, msg + "\n")
        except OSError:
            break

# Method to send message to the chat.
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    try:
        client_socket.send(bytes(msg, "utf8"))
    except OSError:
        print("Error in sending message.")
    if msg == "{quit}":
        client_socket.close()
        window.destroy()

# Action to perform when the window is closed
def on_closing(event=None):
    my_msg.set("{quit}")
    send()

# Method to start the chat main application.
def start_chat():
    global HOST, PORT, ADDR, BUFFSIZE
    
    BUFFSIZE = 1024

    # Get host and port from user
    HOST = str(host_entry.get())
    PORT = int(port_entry.get())
    
    ADDR = (HOST, PORT)
    
    start_window.destroy()

    start_main_application()


def start_main_application():
    global client_socket, receive_thread
    global msg_list, my_msg, window
    
    # Main window
    window = tkt.Tk()
    window.title("Chat")

    message_frame = tkt.Frame(window)

    # Text field
    my_msg = tkt.StringVar()
    my_msg.set("Insert here your text")
    scrollbar = tkt.Scrollbar(message_frame)

    # Messages box
    msg_list = tkt.Listbox(message_frame, height=30, width=75, yscrollcommand=scrollbar.set)
    scrollbar.config(command=msg_list.yview)
    scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
    msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
    msg_list.pack()
    message_frame.pack()

    # Input field
    entry_field = tkt.Entry(window, textvariable=my_msg)
    entry_field.bind("<FocusIn>", lambda event: entry_field.delete(0, tkt.END) if entry_field.get() == "Insert here your text" else None)
    entry_field.bind("<Return>", send)
    entry_field.pack()

    # Send button
    send_button = tkt.Button(window, text="Send", command=send)
    send_button.pack()

    # When closing window
    window.protocol("WM_DELETE_WINDOW", on_closing)

    # Create client socket
    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)
        # Create new thread for client
        receive_thread = Thread(target=receive)
        receive_thread.start()
    except OSError:
        print("Error while initializing connection to server.")
        window.destroy()

    tkt.mainloop()

# Start window
start_window = tkt.Tk()
start_window.title("Setup")

# Input entries for ip and port
tkt.Label(start_window, text="Server IP:").grid(row=0, column=0, padx=10, pady=5)
host_entry = tkt.Entry(start_window)
host_entry.grid(row=0, column=1, padx=10, pady=5)

tkt.Label(start_window, text="Port:").grid(row=1, column=0, padx=10, pady=5)
port_entry = tkt.Entry(start_window)
port_entry.grid(row=1, column=1, padx=10, pady=5)

# Button to start main app
start_button = tkt.Button(start_window, text="Start Chat", command=start_chat)
start_button.grid(row=2, columnspan=2, padx=10, pady=10)


start_window.mainloop()