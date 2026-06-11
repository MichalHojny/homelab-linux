#!/usr/bin/env bash
set -euo pipefail

echo "=== Containers ==="
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'

echo
echo "=== Forwarded ports ==="
echo -n "vpn: "
docker exec vpn sh -c 'cat /tmp/gluetun/forwarded_port 2>/dev/null; echo' || true

echo -n "vpn-deluge: "
docker exec vpn-deluge sh -c 'cat /tmp/gluetun/forwarded_port 2>/dev/null; echo' || true

echo
echo "=== rTorrent port ==="
grep -nE 'network.port_range.set|network.port_random.set' /home/z/rutorrent-hdd/rtorrent/rtorrent.rc || true

echo
echo "=== Deluge port ==="
docker exec -u abc deluge_ssd deluge-console -c /config "config listen_ports random_port" || true
