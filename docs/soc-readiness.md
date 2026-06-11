# SOC Analyst L1 readiness

This document maps my current homelab and operational experience to entry-level SOC Analyst requirements.

## English

Current level: B1+ / working operational English.

I use English documentation, Linux manuals, GitHub issues, Docker documentation, Kubernetes documentation and security-related materials during daily learning.

## Basic cybersecurity knowledge

Current focus areas:

- CIA triad: confidentiality, integrity, availability
- authentication vs authorization
- least privilege
- patching and vulnerability management basics
- network exposure and attack surface
- logs as evidence
- incident triage
- false positive vs true positive
- basic malware/phishing awareness
- VPN, DNS, TLS, HTTP, SSH basics

## Log and event analysis

Practiced through Linux homelab troubleshooting:

- systemd logs with journalctl
- SSH login logs
- Docker container logs
- nginx access and error logs
- VPN/Gluetun logs
- Kubernetes pod status and events
- service failures and restart loops
- DNS and network troubleshooting

Example commands used:

```bash
journalctl -xe
journalctl -u docker
journalctl -u sshd
docker logs CONTAINER
docker ps
ss -tulpn
ip route
ip neigh
dig
curl -v
tcpdump
Operating systems

Linux:

Arch Linux as daily system
Ubuntu and Debian virtual machines
systemd services
SSH
bash
file permissions
mounts and storage
logs
package management
basic firewalling

Windows:

basic end-user and troubleshooting knowledge
willing to strengthen Windows Event Viewer and Sysmon for SOC work
Networking basics

Practiced topics:

DNS
DHCP
TCP/IP
NAT
routing
ports
HTTP/HTTPS
SSH
VPN
reverse proxy
Cloudflare Tunnel
Docker networking
libvirt NAT network

Homelab examples:

libvirt default NAT network: 192.168.122.0/24
VM gateway/DNS through virbr0
fixing VM DNS problems blocked by firewall
nginx reverse proxy
Cloudflare Tunnel to local services
Gluetun VPN containers for isolated torrent clients
Procedures and documentation

Professional background includes content moderation / trust and safety work:

working with procedures
reviewing cases carefully
documenting decisions
following escalation paths
accuracy under repetitive operational work
handling sensitive content according to policy

Homelab documentation approach:

problem
symptoms
commands used
evidence
fix
verification
rollback
Security standards basics

Current study targets:

ISO 27001 basics: information security management, risk, controls
NIST Cybersecurity Framework: Identify, Protect, Detect, Respond, Recover
MITRE ATT&CK basics for mapping suspicious behavior
Analytical thinking

Examples from homelab:

identified VPN endpoint speed problems by testing from inside containers
confirmed missing Proton forwarded port through Gluetun logs
fixed Deluge port configuration through deluge-console
fixed rTorrent forwarded port configuration
diagnosed VM DNS/network problems
verified Docker network isolation with network_mode service:vpn
separated services into containers and VMs
Current gap list

To improve for SOC L1:

Wazuh lab
Windows Event Viewer basics
Sysmon basics
MITRE ATT&CK mapping examples
sample incident reports
basic SIEM alert triage notes
