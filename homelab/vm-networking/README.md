# VM Networking Lab

This module documents the virtual machine networking setup used in the homelab.

## Topology

```text
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
DNS flow

Virtual machines use the libvirt bridge address as DNS:

VM
  ↓
192.168.122.1:53
  ↓
libvirt dnsmasq on host
  ↓
upstream DNS
Important concepts
192.168.122.1 is the libvirt gateway and DNS address for VMs.
192.168.122.10 is srv-01 Ubuntu.
192.168.122.50 is srv-02 Debian.
nginx on srv-02 listens on port 80.
0.0.0.0:80 means nginx listens on all interfaces inside that VM.
A service listening on 0.0.0.0 inside a VM is not automatically exposed to the internet.
Firewall and routing decide what can actually reach a service.
