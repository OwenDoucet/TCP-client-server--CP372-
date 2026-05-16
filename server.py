import socket
import os

#config stuff
HOST = '127.0.0.1'
PORT = 65432

def start_server():
    # Create directory to store uploaded files
    if not os.path.exists('server_files'):
        os.makedirs('server_files')

    #creating tcp socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen() #listening for connections
        print(f"Server has been started on {HOST}, {PORT}. Waiting for client connection...")

        while True:
            #accepting a connection
            conn, addr = s.accept()
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
                            return
                        conn.sendall(message.encode('utf-8'))

                        
                print("Client disconnected")
if __name__ == "__main__":
    start_server()