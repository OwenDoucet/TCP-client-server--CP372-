# TCP client-server application
## Running the Server
Open the *server.py* file and run it

## Running the Client
Open the *client.py* file and run it

You **MUST** run *server.py* first before the client so the client can connect to the server

## Required Dependencies
There are no required dependencies for this project. <br />

All dependencies should already be built into Python <br />
-socket <br />
-os <br />
-threading <br />
-time <br />

## Example Commands
**Client** can: <br />
`LOGIN Kevin` - login server with username "Kevin" <br />
`FILE test.txt` - upload "test.txt" to server <br />
`MSG hello!` - send message to server <br />
`QUIT` - disconnect the server and close client.py <br />


**Server** can: <br />
`QUIT` - close server when all clients have disconnected <br />

## Folder Structure
- README.md
- server_files
    - test.txt
- client.py
- server.py
- test.txt
- users.txt