# Homelab Linux
Personal Linux homelab focused on Linux system administration, 
networking, virtualization, reverse proxying, secure remote 
access, automation and infrastructure troubleshooting. The purpose 
of this project is to build a small but realistic infrastructure 
lab that behaves like a simplified production environment. It is 
used to learn and document how services are deployed, connected, 
secured, backed up and debugged across a Linux host, virtual 
machines and containers. ---
## Goals
- Build practical Linux administration skills through real 
services and real troubleshooting. - Keep public exposure minimal 
and route external access through Cloudflare Tunnel. - Use VMs and 
containers to separate services instead of installing everything 
directly on the host. - Document every important change so the lab 
can be understood, restored and improved over time. - Treat 
troubleshooting notes, rollback steps and backup procedures as 
part of the project. ---
## Current Stack
- Arch Linux host - KVM / libvirt virtualization - Ubuntu and 
Debian virtual machines - Docker / Docker Compose - nginx reverse 
proxy - Apache Guacamole for browser-based remote access - 
Cloudflare Tunnel / DNS / WAF - UFW firewall - Fail2ban hardening 
notes - Git-based documentation - Basic Ansible control node setup 
---
## Architecture Overview
```text [Internet] │ │ [Cloudflare Tunnel] │ ▼ 
                  ┌──────────────────────┐ │ Arch Linux host │ │ 
                  archlinux │ │ LAN: 192.168.1.92 │ 
                  └──────────┬───────────┘
                             │ 
       ┌─────────────────────┼─────────────────────┐ │ │ │ ▼ ▼ ▼
[nginx reverse proxy] [Docker] [libvirt/KVM] localhost/80 docker0 
 virbr0
                        172.17.0.1/16 192.168.122.1/24 br 
                        172.19.0.1/16 Gateway/DNS for VMs
                             │ │ │ │ ┌──────────────────┘ │ │ │ ▼ 
          ▼
 [Guacamole / guacd] ┌──────────────────────┐ guacd: ~172.19.0.4 │ 
 srv-01 Ubuntu │ connects to host RDP │ 192.168.122.10 │ 
 192.168.1.92:3389 │ backend/API :3000 │
                                        └──────────────────────┘ 
                                        ┌──────────────────────┐ │ 
                                        srv-02 Debian │ │ 
                                        192.168.122.50 │ │ nginx 
                                        :80 frontend │
                                        │ proxy to srv-01:3000 │ 
                                        └──────────────────────┘ 
                                        ┌──────────────────────┐ │ 
                                        BlackArch VM │ │ disk: 
                                        /mnt/secure-vms │ │ 
                                        lab/security tools │ │ 
                                        RAM: ~12 GB │ 
                                        └──────────────────────┘ 
                                        ┌──────────────────────┐ │ 
                                        Whonix-Gateway │ │ Tor 
                                        gateway │ │ RAM: ~2 GB │ 
                                        └──────────────────────┘
Network Map Component Address / Network Role Home router 
192.168.1.1 LAN gateway Arch host 192.168.1.92 Main host libvirt 
virbr0 192.168.122.1/24 VM gateway and DNS srv-01 192.168.122.10 
Backend/API server srv-02 192.168.122.50 Frontend/nginx server 
Docker bridge 172.17.0.1/16 Default Docker network Guacamole 
Docker network 172.19.0.0/16 Guacamole / guacd network guacd 
~172.19.0.4 RDP proxy component Host xrdp 192.168.1.92:3389 Remote 
desktop target Ollama 127.0.0.1:11434 Local AI service ruTorrent 
192.168.1.92:9080 Local torrent UI, historical setup Virtual 
Machines srv-01 Item Value OS Ubuntu IP 192.168.122.10 Gateway 
192.168.122.1 DNS 192.168.122.1 Role Backend/API server Backend 
port 3000 Database SQLite Service company-backend.service Ansible 
user ansible srv-02 Item Value OS Debian IP 192.168.122.50 Gateway 
192.168.122.1 DNS 192.168.122.1 Role Frontend/nginx server nginx 
port 80 Reverse proxy srv-01:3000 Ansible user ansible BlackArch 
Item Value VM name blackarch Disk 
/mnt/secure-vms/libvirt/images/blackarch.qcow2 Storage encrypted 
host partition RAM ~12 GB CPU 5 vCPU Role Security tools lab 
BlackArch can consume a lot of memory. It should be stopped when 
running larger local AI models or other memory-heavy workloads. 
Whonix-Gateway Item Value VM name Whonix-Gateway Disk 
/mnt/secure-vms/libvirt/images/whonix-gateway.qcow2 RAM ~2 GB Role 
Tor gateway for isolated testing Projects company-lab A small 
production-like two-server web application. Target architecture: 
Browser
  ↓ srv-02 nginx :80 ↓ / frontend /api/* reverse proxy ↓ srv-01 
backend :3000 Current goals: Add backend health/status/system 
endpoints. Add a professional frontend status dashboard. Route 
frontend API calls through nginx reverse proxy. Manage backend 
with systemd. Add Ansible deployment later. Document deploy, 
rollback and troubleshooting. guacamole Apache Guacamole setup for 
browser-based remote access. Current role: Browser-based access to 
internal systems. guacd container connects to host xrdp. External 
access is intended to go through Cloudflare Tunnel and local 
nginx. Direct public port forwarding is avoided. nginx Local 
reverse proxy configuration. Main purpose: Keep service routing 
centralized. Avoid exposing internal ports directly. Route 
Cloudflare Tunnel traffic to internal services. Keep external 
access controlled and auditable. vm-networking Documentation for 
KVM/libvirt NAT networking, VM DNS and firewall troubleshooting. 
Important solved issue: VMs could reach IP addresses but could not 
resolve domains. Root cause: UFW blocked DNS traffic from VMs to 
libvirt dnsmasq on virbr0. Fix: allow UDP/TCP 53 from virbr0 to 
192.168.122.1. fail2ban Basic Fail2ban configuration and future 
hardening notes. Planned role: Protect exposed authentication 
surfaces. Document jail configuration. Add log-based detection for 
nginx/Guacamole where possible. Design Principles Keep public 
ports closed wherever possible. Use Cloudflare Tunnel for 
controlled external access. Route HTTP services through local 
nginx. Separate services using VMs and containers. Prefer small, 
documented changes over large unclear changes. Always know how to 
test, rollback and restore. Keep secrets out of public Git 
repositories. Store example configs with placeholders instead of 
real tokens, passwords or private domains. Treat troubleshooting 
as part of the project. Build the lab like a small production 
environment. Operational Checks Host checks hostname ip a ip route 
ss -tulpn systemctl --failed libvirt checks virsh -c 
qemu:///system list --all virsh -c qemu:///system net-list --all 
Docker checks docker ps docker network ls docker volume ls nginx 
checks sudo nginx -t systemctl status nginx --no-pager sudo 
journalctl -u nginx -n 100 --no-pager Firewall checks sudo ufw 
status numbered sudo iptables -S Service checks systemctl status 
company-backend --no-pager curl -s 
http://192.168.122.10:3000/health curl -I http://192.168.122.50 
Backup Strategy Current planned strategy: Full system image backup 
to external USB HDD. Important config backup before risky changes. 
Repository and documentation committed to Git. Future documented 
restore procedure. Planned backup layers: Frequency Method Purpose 
Before risky changes quick config copy rollback nginx/UFW/Docker 
changes Weekly config and repo backup restore important files 
Monthly full system image recover from disk/system failure Current 
Status Implemented: Arch Linux host with KVM/libvirt. Default 
libvirt NAT network. Ubuntu and Debian VMs. VM DNS troubleshooting 
through libvirt dnsmasq. UFW rules for VM DNS access. Apache 
Guacamole remote access stack. Basic nginx reverse proxy 
structure. Basic company-lab frontend/backend structure. Basic 
Ansible user access to srv-01 and srv-02. In progress: 
Professional two-server company-lab dashboard. Better deployment 
documentation. Backup and restore procedure. Service hardening. 
Monitoring. Ansible automation. TODO High priority Finish 
company-lab production-like dashboard. Add backend /health, 
/status, /system endpoints. Add nginx /api/ reverse proxy from 
srv-02 to srv-01. Add company-lab documentation. Add backup and 
restore documentation. Medium priority Add Ansible playbooks for 
srv-01 and srv-02. Add monitoring with Uptime Kuma or 
Prometheus/Grafana. Add architecture diagrams as images. Improve 
Fail2ban rules. Add security audit checklist. Later Add Docker 
service template. Add Kubernetes/k3s lab after 
nginx/systemd/Ansible are solid. Add AI infrastructure lab using 
Ollama/vLLM when host resources allow it. Learning Focus This 
homelab is aimed at building practical skills for: Linux 
administration networking and DNS troubleshooting KVM/libvirt 
virtualization Docker and service separation nginx reverse 
proxying secure remote access firewalling and hardening backup and 
disaster recovery Ansible automation
DevOps and future AI infrastructure work
