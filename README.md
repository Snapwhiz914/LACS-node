# LACS node

<p align=center><img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pyyaml"> <img alt="GitHub" src="https://img.shields.io/github/license/Snapwhiz914/LACS-node"> </p>

Before reading...
See the [main](https://github.com/Snapwhiz914/LACS) project.

## Summary
This is an extension of the main project ^ that allows firewall changes to be securely replicated to other servers.

## How it works

1. The main LACS program runs on a different server, and when it wants to change the firewall, it sends a command to its node servers to change thier firewalls.
2. The server running the node program recieves these changes through a simple HTTP API request and adds the allow rule to the firewall, then uses at to schedule its removal.

## Quick start

### 1. Pre-Setup Requirements

 - You'll need a server already running LACS, and access to its configuration file
 - You'll also need access to the configuration file of the server running LACS

### 2. Copy-Paste terminal commands

This code assumes you already have:
 - UFW installed and set up

```bash
git clone https://github.com/Snapwhiz914/LACS-node
cd LACS-node
chmod +x install.sh
./install.sh
```

### 3. Configuring your config

The configuration file will be at /etc/lacs.yaml after running the install instructions above.

Here is a general guide for what your configuration should look like (this is the default config with no comments):

```yaml
key: 7fbuyfhp2hr32rup4
bind_addr: ''
port: 5227
```

Feel free to change anything, but be careful of what you put in for bind_addr.
'0.0.0.0' and '' are equal, and bind to every address on the server, which works in most cases.
If you want it bound to just one address, put that address in instead.

#### Don't forget to update your config on the main server!

1. Get your auto-generated key from /etc/lacs-node.yaml and save it for the next step.
2. Next, you'll need the IP address of the node server that is accessible from the main server.
3. Finally, if you changed your port from the default, make sure you know what it is.

At the bottom of your configuration, add a snipet that looks like this:
```yaml
address: '192.168.0.0'
port: 5227
key: rh473bf83rhu
```

### 4. Starting/stoppping LACS Node

Start LACS Node:
```bash
systemctl start lacs-node.service
```
LACS Node is automatically configured to run on boot through a systemd service.
You must run ```systemctl restart lacs-node.service``` after editing your config.

### 5. Problems? Read the notes

## Notes/Requirments:
 - Any linux OS that supports UFW and python should be able to run this program.
 - The auto-generated key should be secure enough, but it can be anything you like.
 - SSL is not supported for now, mostly because this is supposed to be run on a secure LAN not accessible from the internets

## Contributing

Be sure to read the CONTRIBUTING.md file before you submit a pull request

## Future

 - I'll get SSL support if need be.
