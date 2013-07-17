#!/usr/bin/env python

from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from subprocess import call


class Nagios(LineReceiver):

    def __init__(self):
        self.state = "initialize"

    def connectionMade(self):
        self.sendLine("{'msg':'ack','queues':['nagios']}")
        call(['notify-send', 'Connection made'])

    def dataReceived(self, data):
        if self.state == "initialize":
            self.sendLine("{'msg':'ack','queues':['nagios']}")
            self.state = "initialized"
        else:
            call(['notify-send', data])


def gotProtocol(p):
    p.sendMessage("{'msg':'ack','queues':['nagios','test']}")

point = TCP4ClientEndpoint(reactor, "localhost", 1234)
d = connectProtocol(point, Nagios())
d.addCallback(gotProtocol)
reactor.run()
