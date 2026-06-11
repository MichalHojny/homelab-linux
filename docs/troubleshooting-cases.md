# Troubleshooting case studies

This document contains real troubleshooting cases from my Linux homelab.

Each case follows the same structure:

- problem
- environment
- diagnosis
- root cause
- fix
- verification
- lessons learned

## Case 1: VM DNS blocked by firewall

### Problem

A virtual machine had network access issues and DNS resolution did not work.

### Environment

- Arch Linux host
- libvirt default NAT
- virbr0: 192.168.122.1/24
- VM subnet: 192.168.122.0/24

### Diagnosis

- checked VM IP configuration
- checked gateway and DNS
- checked host firewall
- verified dnsmasq/libvirt DNS on virbr0

### Root cause

Firewall rules blocked DNS traffic from the VM network to the host interface virbr0.

### Fix

Allowed DNS traffic on virbr0 to 192.168.122.1.

### Verification

- VM could resolve domains
- apt, ping and curl worked again
- network route stayed through libvirt NAT

### Lessons learned

- VM networking requires checking IP, gateway, DNS and host firewall
- DNS failures can look like general internet failures

## Case 2: rTorrent had wrong forwarded port

### Problem

rTorrent was slow and the torrent port status was not correct.

### Environment

- ruTorrent/rTorrent container
- Gluetun Proton WireGuard container
- Proton NAT-PMP port forwarding
- Docker Compose



## Case 2: rTorrent had wrong forwarded port

### Problem

rTorrent was slow and the torrent port status was not correct.

### Environment### Diagnosis

- checked Gluetun forwarded port file
- checked rTorrent config
- checked container logs
- compared VPN speed from inside the container

### Root cause

rTorrent had an old static port while Proton assigned a different forwarded port.

### Fix

Added a helper container that reads the Gluetun forwarded port from:

- /tmp/gluetun/forwarded_port

and updates:

- /config/rtorrent/rtorrent.rc

### Verification

- Gluetun showed forwarded_port
- rTorrent config matched the forwarded port
- rTorrent container was restarted after port update

### Lessons learned

- VPN port forwarding can change after restart
- torrent client port must match the provider forwarded port

## Case 3: Deluge port sync failed

### Problem

Deluge did not accept the forwarded port automatically.

### Environment

- Deluge container
- Gluetun Proton WireGuard container
- Docker Compose
- deluge-console

### Diagnosis

- checked Gluetun forwarded port
- checked Deluge logs
- ran deluge-console manually
- checked listen_ports and random_port

### Root cause

deluge-console was executed without the correct user/config path and failed authentication.

### Fix

Used deluge-console as the correct container user with the correct config path.

The important settings were:

- random_port: false
- listen_ports: provider forwarded port

### Verification

- Deluge config showed correct listen_ports
- random_port was false
- helper logs confirmed update

### Lessons learned

- container user and config path matter
- logs showed the exact error: password mismatch

## Case 4: VPN endpoint had speed but no port forwarding

### Problem

A VPN endpoint had acceptable speed but no forwarded port.

### Environment

- Gluetun
- Proton WireGuard
- custom endpoint
- Deluge

### Diagnosis

- ran speedtest inside the VPN container
- checked Gluetun logs
- checked /tmp/gluetun/forwarded_port

### Root cause

The endpoint did not provide working NAT-PMP/port forwarding even though the VPN tunnel worked.

### Evidence

Gluetun showed NAT-PMP connection refused.

### Fix

Changed to another Proton endpoint with P2P and NAT-PMP enabled.

### Verification

- forwarded_port appeared
- Deluge helper updated listen_ports
- VPN public IP and forwarded port were verified

### Lessons learned

- working VPN does not mean working port forwarding
- torrent setup needs both speed and forwarded_port

## Case 5: K3s nginx demo

### Goal

Verify basic Kubernetes workflow on a single-node K3s VM.

### Environment

- Ubuntu VM
- K3s
- 6 vCPU
- 12 GB RAM
- 60 GB disk

### Steps

- installed K3s
- checked node status
- created namespace
- created nginx deployment
- exposed service
- tested port-forward

### Verification

- node Ready
- pod Running
- service reachable through port-forward

### Lessons learned

- basic Kubernetes objects: namespace, deployment, pod and service
- port-forward is useful for local testing
