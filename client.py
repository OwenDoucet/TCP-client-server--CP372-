import socket
import os

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
                
                #LOGIN COMMAND
                if cmd.upper().startswith("LOGIN") or cmd.upper() == "LOGIN":
                    s.sendall(cmd.encode('utf-8'))
                    data = s.recv(1024)
                    print(f"Server response: {data.decode('utf-8')}")

                # MSG command - handle simple message
                elif cmd.upper().startswith("MSG ") or cmd.upper() == "MSG":
                    s.sendall(cmd.encode('utf-8'))
                    data = s.recv(1024)
                    print(f"Server response: {data.decode('utf-8')}")

                # FILE command - handle file upload
                # expect format "FILE filepath" 
                elif cmd.upper().startswith("FILE "):
                    parts = cmd.split(' ', 1)
                    if len(parts) > 1:
                        filepath = parts[1].strip()
                        if os.path.isfile(filepath):
                            filesize = os.path.getsize(filepath)
                            filename = os.path.basename(filepath)
                            
                            # Send intent with filename and automatically calculated size
                            # Format: "FILE filename filesize"
                            s.sendall(f"FILE {filename} {filesize}".encode('utf-8'))
                            
                            resp = s.recv(1024).decode('utf-8')
                            if resp == "READY":
                                with open(filepath, 'rb') as f:
                                    while True:
                                        chunk = f.read(4096)
                                        if not chunk: break
                                        s.sendall(chunk)
                                final_resp = s.recv(1024).decode('utf-8')
                                print(f"Server response: {final_resp}")
                            else:
                                print(f"Server response: {resp}")
                        else:
                            print(f"Error: File '{filepath}' not found")
                
                # case 4: QUIT or other commands - send as is and print response
                else:
                    s.sendall(cmd.encode('utf-8'))
                    if cmd.upper() == "QUIT": break
                    data = s.recv(1024)
                    print(f"Server Response: {data.decode('utf-8')}")
        except ConnectionRefusedError:
            print("Error: server is unavailable")

if __name__ == "__main__":
    start_client()