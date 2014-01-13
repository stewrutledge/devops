#!/usr/bin/env python

from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver
from string import digits, ascii_uppercase
from random import choice
from ast import literal_eval


class Notify(LineReceiver):

    def __init__(self, clients, queues):
        self.clients = clients
        self.client_id = None
        self.state = "INITIAL"
        self.queues = queues

    def gen_client_id(self):
        chars = ascii_uppercase + digits
        return ''.join(choice(chars) for x in range(24))

    def connectionLost(self, reason):
        if self.client_id in self.clients:
            del self.clients[self.client_id]
        for queue in self.queues:
            if self.client_id in self.queues[queue]:
                self.queues[queue].remove(self.client_id)

    def set_id(self, queues):
        client_id = self.gen_client_id()
        self.client_id = client_id
        self.clients[client_id] = self
        for queue in queues:
            if queue not in self.queues:
                self.queues[queue] = []
        for queue in queues:
            self.queues[queue].append(client_id)
        self.state = "INITIALIZED"
        self.sendLine("You have been connected with cliend id: %s" % client_id)
        return client_id

    def lineReceived(self, line):
        try:
            elements = literal_eval(line)
        except:
            if self.state == 'INITIAL':
                self.sendLine("Please register your client: %s"
                              % str("{'msg':'REGISTER', 'queues':"
                                    "['queues', 'to', 'join']}"))
            else:
                self.sendLine("Please send a valid python dict. Example: %s"
                              % str("{'msg':'Danger!', 'queues':['nagios']}"))
        else:
            try:
                elements['key']
            except KeyError:
                key = ""
            else:
                key = elements['key']
            try:
                queues = elements['queues']
                msg = elements['msg']
                if key == '1234':
                    self.broadcast(msg, queues, key=True)
                if self.state == 'INITIAL' and key != '1234':
                    self.set_id(queues)
                elif msg != 'REGISTER':
                    self.broadcast(msg, queues)
            except Exception as e:
                self.sendLine("Error parsing message: %s" % e)

    def broadcast(self, message, queues, key=False):
        for client_id, protocol in self.clients.iteritems():
            for queue in queues:
                to_list = []
                for client in self.queues[queue]:
                    if self.clients[client] != self or key is True:
                        to_list.append(self.clients[client])
        for to in to_list:
            to.sendLine(message)


class NotifyFactory(protocol.Factory):

    def __init__(self):
        self.clients = {}
        self.queues = {}

    def buildProtocol(self, addr):
        return Notify(self.clients, self.queues)

    def makeConnection(self, addr):
        return Notify(self.clients, self.queues)

    def datagramReceived(self, addr, message):
        return Notify(self.clients, self.queues)

port = 1234
reactor.listenTCP(port, NotifyFactory())
reactor.listenUDP(port, NotifyFactory())
print "Broadcast server listening on %s" % port
reactor.run()
