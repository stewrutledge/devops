#/usr/bin/env python

from flask import Flask
from flask import render_template
from flask import request
from ipaddr import IPNetwork
from config import settings


app = Flask(__name__)


@app.route('/<hostname>')
def kickstart(hostname=None):
    ipaddress = request.args.get('ipaddress', None)
    subnet = request.args.get('subnet', None)
    network = IPNetwork(ipaddress + '/' + subnet)
    sp = request.args.get('sp', 'base')
    pp = request.args.get('pp', 'base')
    cp = request.args.get('cp', 'base')
    ep = request.args.get('ep', 'base')
    rp = request.args.get('rp', 'base')
    reg = request.args.get('reg', None)
    gateway = network[1]
    network_root = network[0]
    nameserver = settings.dns_servers[str(network_root)]
    return render_template('base.template',
                           hostname=hostname, subnet=subnet,
                           ipaddress=ipaddress, gateway=gateway,
                           nameserver=nameserver, storage_profile=sp,
                           repo_profile=rp, package_profile=pp,
                           config_profile=cp, extras_profile=ep,
                           reg_profile=reg, root_pw=settings.root_password)

if __name__ == '__main__':
    app.debug = True
    app.run(host='10.50.255.12')
