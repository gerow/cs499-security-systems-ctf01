#!/bin/sh

sudo apt-get install -y python-nfqueue
sudo apt-get install -y python-dpkt
sudo iptables -A FORWARD -p tcp -j NFQUEUE
sudo iptables -A FORWARD -p udp -j NFQUEUE
sudo python sniffer.py
