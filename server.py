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
        print(f"Server has been started on {HOST}, {PORT}. Waiting for client connection...")

        while running:
            conn, addr = s.accept()
            with conn:
                print(f"client connected from {addr}")
                
                while True:
                    #communication between server/client
                    data = conn.recv(1024)
                    if not data:
                        break
                    
                    message = data.decode('utf-8')
                    print(f"Message received: {message}")

                    # check if message is "quit from client"
                    if message.upper() == "QUIT":
                        break

                    conn.sendall(f"ACK: {message}".encode('utf-8'))
                print("Client disconnected")

                #FOR NOW, SERVER TERMINATES WHEN CLIENT CONNECTECTION ENDS
                running = False
                
                
if __name__ == "__main__":
    start_server()
 