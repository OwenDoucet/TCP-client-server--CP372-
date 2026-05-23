import socket
import os
from threading import Thread
import time

#config stuff
HOST = '127.0.0.1'
PORT = 65432

server_run = True


def get_input():
    """
    Get user input from server side
    QUIT (or quit) will terminate server
    """
    global server_run
    while server_run:
        # delay so input text can show up
        time.sleep(0.5)
        server_cmd = input("Server: ")
        # if server command is quit then exit server
        if server_cmd.upper() == "QUIT":
            server_run = False
            print("Server Terminated")

def start_server():
    global server_run 
    # Create directory to store uploaded files
    if not os.path.exists('server_files'):
        os.makedirs('server_files')

    #creating tcp socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen() #listening for connections

        # a 1 second timeout to prevent s.accecpt() from holding
        s.settimeout(1.0)
        print(f"Server has been started on {HOST}, {PORT}. Waiting for client connection...")



        while server_run:
            # try and wait 1 second for connection, if no connection, wait again
            # this is required so thread doesnt lock
            try:
                #accepting a connection
                conn, addr = s.accept()
            except socket.timeout:
                continue
            with conn:
                print(f"client connected from {addr}")
                
                authenticated = False

                while True:
                    #communication between server/client
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    # step 1. convert bytes to string 
                    try:
                        message = data.decode('utf-8')
                    except UnicodeDecodeError:
                        message = ""
                    
                    #login handling
                    if message.upper().startswith("LOGIN "):
                        parts = message.split(' ', 1)
                        if len(parts) > 1:
                            username = parts[1].strip()

                            if not os.path.exists("users.txt"):
                                with open("users.txt", "w") as f:
                                    f.write("Owen\nLeonie\nKevin")
                            
                            with open("users.txt", "r") as f:
                                valid_users = [line.strip() for line in f.readlines()]

                            if username in valid_users:
                                authenticated = True
                                print(f"User '{username}' successfully authenticated.")
                                conn.sendall(f"ACK: Welcome {username}!".encode('utf-8'))
                            else:
                                print(f"Failed login attempt for username: '{username}'")
                                conn.sendall(b"ERR: Access Denied. Invalid Username.")
                        else:
                            conn.sendall(b"ERR: Usage: LOGIN username")
                    
                    elif not authenticated:
                        if message.upper() == "QUIT":
                            print("Unauthenticated client requested to quit.")
                            server_run = False
                            break
                        conn.sendall(b"ERR: You must LOGIN first.")
                    # step 2. FILE
                    # expect format "FILE filename filesize" and handle file upload
                    elif message.upper().startswith("FILE "):
                        parts = message.split()
                        if len(parts) >= 3:
                            filename = parts[1]
                            try:
                                filesize = int(parts[2])
                                conn.sendall(b"READY")
                                
                                filepath = os.path.join('server_files', filename)
                                received = 0
                                with open(filepath, 'wb') as f:
                                    while received < filesize:
                                        chunk = conn.recv(min(4096, filesize - received))
                                        if not chunk: break
                                        f.write(chunk)
                                        received += len(chunk)
                                print(f"File {filename} received ({filesize} bytes)")
                                conn.sendall(f"ACK: File {filename} uploaded successfully".encode('utf-8'))
                            except ValueError:
                                conn.sendall(b"ACK: Invalid file size format")
                        else:
                            conn.sendall(b"ACK: Invalid FILE command format")

                   # step 2 - case 2: QUIT or other messages
                    else:
                        if message.upper() == "QUIT":
                            print("Client requested to quit.")
                            server_run = False
                            break
                        if message.upper().startswith("MSG "):
                            parts = message.split(' ', 1)
                            msg_content = parts[1] if len(parts) > 1 else ""
                            print(f"Message receieved: {msg_content}")
                            conn.sendall(b"ACK: message.received")
                        else:
                            print(f"Invalid protocol command received: {message}")
                            conn.sendall(b"ERR: Invalid Command. Use MSG, FILE, or QUIT.")

                        
                print("Client disconnected")

                # Force print this line cause threading
                print("\rServer: ", end="", flush=True)
                
if __name__ == "__main__":
    # added threading support
    t1 = Thread(target=start_server)
    t2 = Thread(target=get_input)
    t2.daemon = True

    t1.start()
    t2.start()

    t1.join()