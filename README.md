# Homelab Linux

Practical Linux homelab focused on system administration, networking, Docker, virtualization, monitoring and troubleshooting.

This repository documents my hands-on learning path toward Junior Linux Administrator, Technical Support, NOC or SOC L1 roles.

## What I built

- Arch Linux host used as main lab machine
- KVM/libvirt virtual machines
- Ubuntu and Debian server VMs
- Docker and Docker Compose services
- nginx reverse proxy
- Cloudflare Tunnel for remote access
- Prometheus, Grafana, Loki and cAdvisor monitoring stack
- Apache Guacamole remote access
- K3s single-node Kubernetes lab
- VPN-isolated torrent stack with Gluetun, rTorrent and Deluge
- Basic backup and recovery procedures
- Terraform and Ansible lab for repeatable VM deployment

## Main skills shown here

- Linux administration
- SSH and systemd
- DNS, DHCP, TCP/IP and NAT troubleshooting
- Docker networking and bind mounts
- KVM/libvirt VM networking
- nginx reverse proxying
- Cloudflare Tunnel setup
- monitoring and log collection
- basic Kubernetes with K3s
- infrastructure documentation
- troubleshooting and rollback thinking

## Current lab structure

```text
Arch Linux host
├── Docker services
│   ├── monitoring stack
│   ├── Guacamole
│   ├── Jellyfin
│   └── VPN-isolated torrent clients
├── KVM/libvirt VMs
│   ├── Ubuntu / Debian servers
│   ├── K3s lab
│   └── security lab VMs
├── nginx reverse proxy
└── Cloudflare Tunnel
Selected projects
company-lab

Small two-server web application lab.

frontend VM with nginx
backend VM with FastAPI
SQLite database
systemd service
Ansible deployment

Path:

company-lab/
homelab/ansible/
Terraform libvirt lab

Repeatable VM provisioning with Terraform and libvirt.

Includes:

cloud-init
static VM IPs
SSH user injection
Ubuntu cloud images
Terraform apply/destroy workflow

Path:

homelab/terraform/libvirt-company-lab/
Monitoring stack

Docker-based monitoring and logging.

Includes:

Prometheus
Grafana
Loki
Promtail
node-exporter
cAdvisor
K3s lab

Single-node Kubernetes lab used to practice:

namespaces
deployments
pods
services
port-forwarding
Troubleshooting examples

Real problems solved in this lab:

VM DNS blocked by firewall on libvirt bridge
Docker container path and permission issues
rTorrent/Deluge VPN port forwarding issues
Gluetun Proton WireGuard endpoint testing
nginx and Cloudflare Tunnel routing
K3s service and pod checks
storage cleanup and VM disk analysis
Why this repo exists

This is my public technical portfolio.

It shows practical work with Linux, networking, containers, virtual machines, monitoring and troubleshooting instead of only theory.

Security note

No real passwords, tokens, private keys, WireGuard configs, .env files or private tracker data should be committed.

## Homelab projects

- [Torrent stack](homelab/torrent-stack/README.md)
