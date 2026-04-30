
VM Networking

This document describes the current virtual machine networking setup used in the homelab.

The environment is based on an Arch Linux host running KVM/libvirt. Virtual machines are connected through the default libvirt NAT network.

Network layout
Arch Linux host
├── LAN interface: enp3s0
│   └── IP: 192.168.1.92/24
│
├── libvirt bridge: virbr0
│   └── IP: 192.168.122.1/24
│
├── VM: srv-01 Ubuntu
│   └── IP: 192.168.122.10/24
│
└── VM: srv-02 Debian
    ├── IP: 192.168.122.50/24
    └── nginx: port 80
Addressing
SystemRoleIP address
Arch hostHypervisor / gateway for VMs192.168.1.92
virbr0libvirt bridge / VM gateway / VM DNS192.168.122.1
srv-01Ubuntu VM192.168.122.10
srv-02Debian VM / nginx test server192.168.122.50
DNS flow

Virtual machines use the libvirt bridge address as their DNS server:

VM
  ↓
192.168.122.1:53
  ↓
libvirt dnsmasq on host
  ↓
upstream DNS

In this setup, 192.168.122.1 is not nginx and not a general application server. It is the host-side libvirt bridge address used by VMs as their gateway and DNS endpoint.

Important concepts
192.168.122.1 is the libvirt gateway and DNS address for VMs.
192.168.122.10 is srv-01 running Ubuntu.
192.168.122.50 is srv-02 running Debian.
nginx on srv-02 listens on port 80.
0.0.0.0:80 means nginx listens on all interfaces inside that VM.
A service listening on 0.0.0.0 inside a VM is not automatically exposed to the internet.
Routing, NAT and firewall rules decide what can actually reach a service.
Troubleshooting notes
Symptom

The VM can ping IP addresses, but DNS names do not resolve.

Example:

ping 9.9.9.9        works
ping google.com    fails
Meaning

Routing works, but DNS does not.

The VM can reach the internet by IP address, but cannot resolve domain names.

Cause found

The host firewall was blocking DNS traffic from the VM network to libvirt dnsmasq on virbr0.

Fix

Allow DNS traffic from VMs to the libvirt bridge address:

sudo ufw allow in on virbr0 to 192.168.122.1 port 53 proto udp
sudo ufw allow in on virbr0 to 192.168.122.1 port 53 proto tcp

UDP is required for normal DNS queries. TCP is useful for larger DNS responses and fallback behavior.

Useful checks

Check libvirt network status:

virsh net-list --all

Check host bridge address:

ip addr show virbr0

Check DNS listener on the host:

ss -tuln | grep ':53'

Check VM routing:

ip route

Check VM DNS configuration:

cat /etc/resolv.conf

Test DNS from a VM:

ping 9.9.9.9
ping google.com
Current status

The VM network is working.

VMs can reach the host bridge.
VMs can use 192.168.122.1 as gateway.
DNS works through libvirt dnsmasq.
UFW allows DNS from the VM network to virbr0.
srv-02 nginx is reachable internally on port 80.
