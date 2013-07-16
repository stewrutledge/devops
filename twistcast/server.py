#!/usr/bin/env python

from twisted.internet import protocol, reactor
from twisted.protocols.basic import LineReceiver
import string
import random


class Notify(LineReceiver):

    def __init__(self, clients):
        self.clients = clients
        self.client_id = None
        self.state = "INITIAL"

    def gen_client_id(self):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for x in range(6))

    def connectionLost(self, reason):
        if self.client_id in self.clients:
            del self.clients[self.client_id]

    def set_id(self, client_id):
        self.sendLine("Connection made. Client id: %s" % (client_id,))
        self.client_id = client_id
        self.clients[client_id] = self
        self.state = "INITIALIZED"

    def lineReceived(self, line):
        key = line.split(',')
        if key[0] == '1234':
            line = key[1]
        if self.state == 'INITIAL' and key[0] != '1234':
            gened_id = self.gen_client_id()
            self.set_id(gened_id)
        else:
            self.broadcast(line)

    def broadcast(self, message):
        for client_id, protocol in self.clients.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class NotifyFactory(protocol.Factory):

    def __init__(self):
        self.clients = {}

    def buildProtocol(self, addr):
        return Notify(self.clients)

port = 1234
reactor.listenTCP(port, NotifyFactory())
print "Broadcast server listening on %s" % port
reactor.run()
