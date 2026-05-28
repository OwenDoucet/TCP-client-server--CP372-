# TCP client-server application
## Running the Server
Open the server.py file and run it

## Running the Client
Open the client.py file and run it

You **MUST** run server.py first before the client so the client can connect to the server

## Required Dependencies
There are no required dependencies for this project.
All dependencies should already be built into Python
-socket
-os
-threading
-time

## Example Commands
Client can:
LOGIN Kevin - login server with username "Kevin"
FILE test.txt - upload "test.txt" to server
MSG hello! - send message to server
QUIT - disconnect the server and close client.py


Server can:
QUIT - close server when all clients have disconnected

## Folder Structure
>README.md
>server_files
-->test.txt
>client.py
>server.py
>test.txt
>users.txt