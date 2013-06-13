# A simple flask webapp for generating kickstart files

## Getting Started

I don't have a setup script or anything (yet) but all that is really needed is flask and  ipaddr (used for converting the ipadress and subnet to CIDR notation for matching in the config/settings.py file.

I plan on eventually removing this requirement and trying to keep as much in the stdlib as possible.

After starting the flask app (you will need to had app.run(host='yourmachinesip') in order to access it from anywhere besides localhost, or set it up with apache) browse to:

http://yourip:5000/hostname.example.com?ipaddress=192.168.0.10&subnet=255.255.255.0

This will build a kickstarter with the hostname hostname.example.com and ip/subnet combo provided. There are futher paramaters that can be filled in for registration and other template profiles, but if nothing is provided it defaults to the "base" profiles.

## Template files

There are a number of template files included in the repository, a sort of base (though by no means anything I am advocating as best practice) settings.

The idea is that everyting after the _ in the template name is the profile name. So for example "storage_base" is the default configuration that needs to be used. In order to change it, add a template with a name like "storage_huge.template" and in the URL providel sp=huge. The following parameters are excepted:

- sp = storage_profile (the hard drive layout)
- rp = repos_profile (for adding repositories before package installation)
- pp = packages_profile (what packages are installed)
- cp = config_profile (any additional configuration done after package installation)
- ep = extras_profile (anything you don't think fits here, ran at the end of the kickstart file)
- reg = registration for redhat network (default is no registration, so it works with centos)

So at it's largest the URL could look like:

> http://yourip:5000/host.example.com?ipaddress=192.168.0.2&subnet=255.255.255.0&sp=huge&cp=external&rp=geleranode&ep=prettybash&reg=globalcom

TODO: 
- Make things like repo_config able to pull together several repository files to build profiles more dynamically and lower the number of total template files needed.
- Add support for DHCP (right now a static ip is required)

## config/settings.py

The config file is pretty empty, right now is just a list for matching name servers to subnets and a root password (encrypted)

To generate a root password type into your shell:

> python -c "import crypt, getpass, pwd; print crypt.crypt('YOURPASSWORD', '\$6\$YOURSALT\$')"

The password is, for now, stored along side the salt. It would be nice to seperate these too.

That's more or less it!
