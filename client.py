import socket

#config
HOST = '127.0.0.1'
PORT = 65432

def start_client():
    #tcp socket stuff
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((HOST, PORT))
            print("Connected to server")

            while True:
                #user input
                cmd = input("> ")
                if not cmd: continue

                s.sendall(cmd.encode('utf-8'))

                if cmd.upper() == "QUIT": break
                data = s.recv(1024)
                print(f"Server response: {data.decode('utf-8')}")
        except ConnectionRefusedError:
            print("Error: server is unavailable")

if __name__ == "__main__":
    start_client()