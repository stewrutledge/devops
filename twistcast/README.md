# Twistcast

A simple twisted based client/server setup for broadcasting messages to gnomes notify service
Currently calls the binary for notify-send on the client side, this is obviously suboptimal but it reduces the dependencies in python to just twisted

## Server
The server listens for connections, and when made assigns a 6 character random id to every client. If connecting via telnet, a message needs to first be sent to initialize this connection and get assigned an id.

For the sake of integrating other applications (for example nagios warnings) you can skip the initialization phase by entering a key, currently seperated by a comma, for example:

> echo "1234,WARNING WARNING"|nc broadcasthost 1234

Will bypass the assignment of and ID and simply broadcast a message to all connected clients.

## Client

Nothing special here, just run it and you're connected. The hostname/ip address and port need to match the server.
