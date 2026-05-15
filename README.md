# Homelab Linux

Personal Linux homelab focused on system administration, networking, virtualization, secure remote access, reverse proxying, automation and infrastructure troubleshooting.

This repository documents a small but realistic lab environment built on an Arch Linux host. The goal is to learn Linux administration through real services, real network problems and real recovery procedures.

## Project goals

- Learn Linux administration through practical infrastructure work.
- Keep public ports closed whenever possible.
- Use Cloudflare Tunnel as the external entry point.
- Route HTTP services through a local nginx reverse proxy.
- Separate services using VMs and containers.
- Document configuration, troubleshooting, rollback and restore steps.
- Build a portfolio-quality homelab that can be explained during job interviews.

## Current stack

| Area | Technology |
|---|---|
| Host OS | Arch Linux |
| Virtualization | KVM / libvirt |
| VMs | Ubuntu, Debian, BlackArch, Whonix Gateway |
| Containers | Docker / Docker Compose |
| Reverse proxy | nginx |
| Remote access | Apache Guacamole |
| External access | Cloudflare Tunnel |
| Firewall | UFW |
| Hardening | Fail2ban notes |
| Automation | Ansible basics |
| Documentation | Git / GitHub |

## High-level architecture

External traffic is routed through Cloudflare Tunnel into the Arch host. The host uses nginx as a local reverse proxy and routes traffic to internal services, VMs and containers.

| Layer | Component | Role |
|---|---|---|
| Internet edge | Cloudflare Tunnel | External entry point without opening router ports |
| Host | Arch Linux | Main hypervisor and service host |
| Reverse proxy | nginx | Local routing to internal HTTP services |
| Containers | Docker | Guacamole and other containerized services |
| Virtualization | libvirt/KVM | VM environment for lab servers |
| Remote access | Guacamole | Browser-based access to internal systems |
| Firewall | UFW | Host-level traffic control |

## Network map

| Component | Address / Network | Role |
|---|---:|---|
| Home router | `192.168.1.1` | LAN gateway |
| Arch host | `192.168.1.92` | Main host |
| libvirt bridge | `192.168.122.1/24` | VM gateway and DNS |
| srv-01 | `192.168.122.10` | Backend/API server |
| srv-02 | `192.168.122.50` | Frontend/nginx server |
| Docker default bridge | `172.17.0.1/16` | Default Docker network |
| Guacamole network | `172.19.0.0/16` | Guacamole / guacd network |
| guacd | `~172.19.0.4` | RDP proxy component |
| Host xrdp | `192.168.1.92:3389` | Remote desktop target |
| Ollama | `127.0.0.1:11434` | Local AI service |
| ruTorrent | `192.168.1.92:9080` | Historical local torrent UI |

## Virtual machines

### srv-01

| Item | Value |
|---|---|
| OS | Ubuntu |
| IP | `192.168.122.10` |
| Gateway | `192.168.122.1` |
| DNS | `192.168.122.1` |
| Role | Backend/API server |
| Backend port | `3000` |
| Database | SQLite |
| Service | `company-backend.service` |
| Ansible user | `ansible` |

### srv-02

| Item | Value |
|---|---|
| OS | Debian |
| IP | `192.168.122.50` |
| Gateway | `192.168.122.1` |
| DNS | `192.168.122.1` |
| Role | Frontend/nginx server |
| nginx port | `80` |
| Reverse proxy target | `srv-01:3000` |
| Ansible user | `ansible` |

### BlackArch

| Item | Value |
|---|---|
| VM name | `blackarch` |
| Disk | `/mnt/secure-vms/libvirt/images/blackarch.qcow2` |
| Storage | Encrypted host partition |
| RAM | ~12 GB |
| CPU | 5 vCPU |
| Role | Security tools lab |

BlackArch can consume a lot of memory. It should be stopped when running larger local AI models or other memory-heavy workloads.

### Whonix Gateway

| Item | Value |
|---|---|
| VM name | `Whonix-Gateway` |
| Disk | `/mnt/secure-vms/libvirt/images/whonix-gateway.qcow2` |
| RAM | ~2 GB |
| Role | Tor gateway for isolated testing |

## Main projects

### company-lab

A small production-like two-server web application.

Architecture:

- Browser connects to `srv-02`.
- `srv-02` serves the frontend through nginx.
- nginx proxies `/api/` requests to `srv-01:3000`.
- `srv-01` runs the backend API as a systemd service.

Planned improvements:

- Add backend endpoints: `/health`, `/status`, `/system`.
- Add a professional frontend status dashboard.
- Add nginx `/api/` reverse proxy.
- Add deployment and rollback documentation.
- Add Ansible deployment later.

### guacamole

Apache Guacamole setup for browser-based remote access.

Current role:

- Browser-based remote access to internal systems.
- guacd connects to host xrdp.
- External access is intended to go through Cloudflare Tunnel and local nginx.
- Direct public port forwarding should be avoided.

### nginx

Local reverse proxy configuration.

Main purpose:

- Centralize HTTP routing.
- Avoid exposing internal service ports directly.
- Route Cloudflare Tunnel traffic to internal services.
- Keep service access controlled and documented.

### vm-networking

Documentation for KVM/libvirt NAT networking, VM DNS and firewall troubleshooting.

Important solved issue:

- VMs could reach IP addresses but could not resolve domains.
- Root cause: UFW blocked DNS traffic from VMs to libvirt dnsmasq on `virbr0`.
- Fix: allow UDP/TCP 53 from `virbr0` to `192.168.122.1`.

### fail2ban

Basic Fail2ban configuration and future hardening notes.

Planned role:

- Protect exposed authentication surfaces.
- Document jail configuration.
- Add log-based protection for nginx and Guacamole where possible.

## Design principles

1. Keep public ports closed wherever possible.
2. Use Cloudflare Tunnel for controlled external access.
3. Route HTTP services through local nginx.
4. Separate services using VMs and containers.
5. Prefer small, documented changes over large unclear changes.
6. Always know how to test, rollback and restore.
7. Keep secrets out of public Git repositories.
8. Store example configs with placeholders instead of real passwords, tokens or private domains.
9. Treat troubleshooting as part of the project.
10. Build the lab like a small production environment.

## Operational checks

| Area | Command |
|---|---|
| Hostname | `hostname` |
| IP addresses | `ip a` |
| Routing | `ip route` |
| Listening ports | `ss -tulpn` |
| Failed services | `systemctl --failed` |
| VMs | `virsh -c qemu:///system list --all` |
| libvirt networks | `virsh -c qemu:///system net-list --all` |
| Docker containers | `docker ps` |
| Docker networks | `docker network ls` |
| nginx config test | `sudo nginx -t` |
| nginx status | `systemctl status nginx --no-pager` |
| UFW rules | `sudo ufw status numbered` |
| Backend status | `systemctl status company-backend --no-pager` |
| Backend health | `curl -s http://192.168.122.10:3000/health` |
| Frontend check | `curl -I http://192.168.122.50` |

## Backup strategy

Current planned strategy:

- Full system image backup to external USB HDD.
- Important config backup before risky changes.
- Repository and documentation committed to Git.
- Future documented restore procedure.

| Frequency | Method | Purpose |
|---|---|---|
| Before risky changes | Quick config copy | Rollback nginx, UFW or Docker changes |
| Weekly | Config and repository backup | Restore important files |
| Monthly | Full system image | Recover from disk or system failure |

## Current status

Implemented:

- Arch Linux host with KVM/libvirt.
- Default libvirt NAT network.
- Ubuntu and Debian VMs.
- VM DNS troubleshooting through libvirt dnsmasq.
- UFW rules for VM DNS access.
- Apache Guacamole remote access stack.
- Basic nginx reverse proxy structure.
- Basic company-lab frontend/backend structure.
- Basic Ansible user access to srv-01 and srv-02.

In progress:

- Professional two-server company-lab dashboard.
- Better deployment documentation.
- Backup and restore procedure.
- Service hardening.
- Monitoring.
- Ansible automation.

## Roadmap

### High priority

- Finish company-lab production-like dashboard.
- Add backend `/health`, `/status`, `/system` endpoints.
- Add nginx `/api/` reverse proxy from srv-02 to srv-01.
- Add company-lab documentation.
- Add backup and restore documentation.

### Medium priority

- Add Ansible playbooks for srv-01 and srv-02.
- Add monitoring with Uptime Kuma or Prometheus/Grafana.
- Add architecture diagrams as images.
- Improve Fail2ban rules.
- Add security audit checklist.

### Later

- Add Docker service template.
- Add Kubernetes/k3s lab after nginx, systemd and Ansible are solid.
- Add AI infrastructure lab using Ollama or vLLM when host resources allow it.

## Learning focus

This homelab is aimed at building practical skills for:

- Linux administration
- networking and DNS troubleshooting
- KVM/libvirt virtualization
- Docker and service separation
- nginx reverse proxying
- secure remote access
- firewalling and hardening
- backup and disaster recovery
- Ansible automation
- DevOps and future AI infrastructure work
