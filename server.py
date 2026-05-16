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

        s.settimeout(1.0)
        print(f"Server has been started on {HOST}, {PORT}. Waiting for client connection...")



        while server_run:
            #accepting a connection
            try:
                conn, addr = s.accept()
            except socket.timeout:
                continue
            with conn:
                print(f"client connected from {addr}")
                
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
                    
                    # step 2. FILE
                    # expect format "FILE filename filesize" and handle file upload
                    if message.upper().startswith("FILE "):
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
                        print(f"Message received: {message}")
                        if message.upper() == "QUIT":
                            print("Client requested to quit. Shutting down server.")
                            break
                        conn.sendall(message.encode('utf-8'))

                        
                print("Client disconnected")
if __name__ == "__main__":
    # added threading support
    t1 = Thread(target=start_server)
    t2 = Thread(target=get_input)
    t2.daemon = True

    t1.start()
    t2.start()

    t1.join()