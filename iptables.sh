#!/bin/bash
set -e
set -x

# Initialize rules
iptables -F

# Deny all accesses from the outside
# Allow any access from the inside
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback interface
iptables -A INPUT -i lo -j ACCEPT

# Allow accesses after session is established
iptables -A INPUT -m state --state ESTABLISHED,RELATED --jump ACCEPT

# Allow SSH accesses from HDE Office
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Continue to use above settings after iptables reloaded
iptables-save
