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

    def set_id(self, queues):
        client_id = self.gen_client_id()
        self.sendLine("Connection made. Client id: %s" % (client_id,))
        self.client_id = client_id
        self.clients[client_id] = self
        for queue in queues:
            if queue not in self.queues:
                self.queues[queue] = []
        for queue in queues:
            self.queues[queue].append(client_id)
        self.state = "INITIALIZED"

    def lineReceived(self, line):
        elements = literal_eval(line)
        try:
            elements['key']
        except KeyError:
            key = ""
        else:
            key = elements['key']
        queues = elements['queues']
        msg = elements['msg']
        if key == '1234':
            self.broadcast(msg, queues)
        if self.state == 'INITIAL' and key != '1234':
            self.set_id(queues)
        else:
            self.broadcast(msg, queues)

    def broadcast(self, message, queues):
        for client_id, protocol in self.clients.iteritems():
            for queue in queues:
                to_list = []
                for client in self.queues[queue]:
                    if self.clients[client] != self:
                        to_list.append(self.clients[client])
        for to in to_list:
            to.sendLine(message)


class NotifyFactory(protocol.Factory):

    def __init__(self):
        self.clients = {}
        self.queues = {}

    def buildProtocol(self, addr):
        return Notify(self.clients, self.queues)

port = 1234
reactor.listenTCP(port, NotifyFactory())
print "Broadcast server listening on %s" % port
reactor.run()
