#!/usr/bin/env python
"""
Simple nagios check for warning when a certificate is going to expire
Author: Stewart Rutledge <stew.rutledge@gmail.com>
Licensed under the MIT License
"""

from datetime import datetime
from ssl import get_server_certificate
from OpenSSL import crypto
from sys import exit
from optparse import OptionParser

usage = ("Usage: %prog [options] url \n"
        "Example: %prog -w 45 -c 30 -p 4343 secure.example.com")
parser = OptionParser(usage)
parser.add_option("-w", "--warn", type="int", dest="warn", default=30,
                  help="Warn threshold in days [default: %default]")
parser.add_option("-c", "--critical", type="int", dest="critical", default=15,
                  help="Critical threshold in days [default: %default]")
parser.add_option("-p", "--port", type="int", dest="port", default=443,
                  help="SSL port [default: %default]")

(options, args) = parser.parse_args()

if len(args) == 0:
    parser.print_help()
    exit(1)

if options.warn < options.critical:
    print("Critical threshhold cannot be larger than warn threshhold")
    exit(1)

try:
    cert = get_server_certificate((args[0], options.port))
except Exception as E:
    print("Could not get certificate: %s" % E)
    exit(3)

try:
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
except Exception as E:
    print("Could not parse certificate: %s" % E)

expires_on = datetime.strptime(x509.get_notAfter(), '%Y%m%d%H%M%SZ')
days_left = expires_on - datetime.today()
 
if days_left.days < options.warn and days_left.days > options.critical:
    print("Warning! %s days left until certificate expires" % days_left.days)
    exit(1)
elif days_left.days < options.critical:
    print("Critical! %s days left until certificate expires" % days_left.days)
    exit(2)
elif days_left.days > options.warn:
    print("OK! %s days left until certificate expires" % days_left.days)
    exit(0)
else:
    print("Something went wrong")
    exit(3)
