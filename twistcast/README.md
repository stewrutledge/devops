# Twistcast

A simple twisted based client/server setup for broadcasting messages to gnomes notify service
Currently calls the binary for notify-send on the client side, this is obviously suboptimal but it reduces the dependencies in python to just twisted.
The server itself listens for python dicts in the format of: 
```python
{'msg':'text to broadcast','queues':['list', 'of', 'queues']}
```

## Server
The server listens for connections, and when made assigns a 24 character random id to every client. If connecting via telnet, a message needs to first be sent to initialize this connection and get assigned an id.



For the sake of integrating other applications (for example nagios warnings) you can skip the initialization phase by entering a key:
```python
{'msg':'SERVER DONE BROKE','queues':['nagios'], 'key':'1234'}
```
This will bypass the assignment of and ID and simply broadcast a message to all connected clients.

## Client

I haven't yet implemented a settings file here, so to specify queues you need to go in and change them, both in the connectionMade function and the dataReceived function (the connectionMade initializes what queues you are a member of, the second one in data receives registers you on the server).

Otherwise, the hostname/ip address and port need to match the server.
