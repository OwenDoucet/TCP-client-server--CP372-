import socket
from threading import Thread


#config stuff
HOST = '127.0.0.1'
PORT = 65432

running = True
        
def start_server():
    global running
    #creating tcp socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen() #listening for connections

        # a 1 second timeout to prevent s.accecpt() from holding
        s.settimeout(1.0)
        print(f"Server has been started on {HOST}, {PORT}. Waiting for client connection...")

        while running:
            conn, addr = s.accept()
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

                    # check if message is "quit from client"
                    if message.upper() == "QUIT":
                        break

                    conn.sendall(f"ACK: {message}".encode('utf-8'))
                print("Client disconnected")

                #FOR NOW, SERVER TERMINATES WHEN CLIENT CONNECTECTION ENDS
                running = False
                
                
if __name__ == "__main__":
    start_server()
 
