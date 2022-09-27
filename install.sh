#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "This must be run as root. No exceptions (limitation of UFW)."
  exit
fi

#Install packages
#Uninstall in case already installed
python3 -m pip uninstall -y lacs-node

if python3 -m pip install .; then
    echo "Package install succeeded."
else
    echo "Package install failed! Check and resolve using errors above."
    exit
fi


echo "Making sure at is installed..."
apt install at

#Create a config file

KEY=$(echo $RANDOM | md5sum | head -c 20; echo;)
CONFIG_TEMPLATE="key: $KEY
bind_addr: ''
port: 5227
"

if [ -f "/etc/lacs-node.yaml" ]
then
    echo "/etc/lacs-node.yaml has already been created, not overwriting..."
else
    touch /etc/lacs-node.yaml
    echo "$CONFIG_TEMPLATE" > /etc/lacs-node.yaml
fi

#Create a systemd service file so it will start on boot
SYSTEMD_FILE=$'[Unit]
Description=LACS Node
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
User=root
ExecStart=start-LACS-node

[Install]
WantedBy=multi-user.target'
touch /lib/systemd/system/lacs_node.service
echo "$SYSTEMD_FILE" > /lib/systemd/system/lacs_node.service
systemctl daemon-reload
if systemctl enable lacs_node.service ; then
    echo "Service installed successfully. LACS Node will run on boot."
else
    echo "Service install failed! Check for errors above"
    exit
fi

echo "Your auto-generated key: $KEY"
echo "Done. Have fun with a secure system. Make sure to edit your configuration file at /etc/lacs-node.yaml, then run systemctl start lacs-node.service."
echo "Check the output above and make sure at was installed."