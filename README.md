# Homelab Linux

Personal Linux homelab focused on system administration, networking, virtualization, remote access and self-hosted infrastructure.

The goal of this project is to build a small but realistic lab environment for learning and documenting Linux administration tasks: VM networking, reverse proxying, firewall rules, remote access, service separation and troubleshooting.

## Current stack

- Arch Linux host
- KVM / libvirt virtualization
- Ubuntu and Debian virtual machines
- Nginx reverse proxy
- Apache Guacamole for remote access
- Docker Compose
- Cloudflare Tunnel / DNS / WAF
- UFW firewall
- Fail2ban
- Git-based documentation

## Current architecture

```text
Internet
  ↓
Cloudflare
  ↓
Cloudflare Tunnel
  ↓
local nginx reverse proxy
  ↓
internal services / VMs / containers

The public entry point is handled through Cloudflare. Public ports on the home router are intended to stay closed. Internal services are routed locally through nginx whenever possible.

Lab layout
Arch Linux host
├── KVM / libvirt
│   ├── srv-01 Ubuntu
│   └── srv-02 Debian
│
├── Docker
│   └── Guacamole / guacd
│
├── nginx
│   └── local reverse proxy
│
└── UFW / Fail2ban
Documentation
homelab/vm-networking

VM networking, libvirt NAT, DNS troubleshooting and UFW rules.
homelab/guacamole

Remote access setup using Apache Guacamole.
homelab/nginx

Local reverse proxy configuration.
homelab/fail2ban

Basic Fail2ban configuration and planned hardening.
Main design principles
Keep the host as clean as possible.
Run services inside VMs or containers where it makes sense.
Keep public ports closed.
Use Cloudflare Tunnel for external access.
Route internal HTTP services through nginx.
Prefer small, documented changes over large unclear changes.
Treat troubleshooting notes as part of the project.
Current status

Implemented:

Arch Linux host with libvirt/KVM
Default libvirt NAT network
Ubuntu and Debian test VMs
VM DNS troubleshooting through libvirt dnsmasq
UFW rules for VM DNS access
Guacamole remote access
Basic nginx reverse proxy structure

In progress:

Company-style lab with separated frontend and backend services
Better documentation structure
Service hardening
Backup and restore procedure
TODO
Document the company-lab project
Add nginx reverse proxy examples for internal services
Add backup and restore documentation
Improve Fail2ban rules
Add monitoring notes
Add diagrams for network and service flow
