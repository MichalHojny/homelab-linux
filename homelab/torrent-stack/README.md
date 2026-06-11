# Torrent Stack

Docker Compose torrent stack for the homelab.

This setup uses two separate VPN containers and two torrent clients:

- rTorrent / ruTorrent for HDD storage
- Deluge for SSD downloads
- Gluetun with Proton WireGuard
- automatic forwarded port sync

## Architecture

```text
Docker host
├── vpn
│   └── rutorrent_hdd
│
└── vpn-deluge
    └── deluge_ssd
```

## Services

| Service | Purpose |
|---|---|
| `vpn` | Gluetun VPN container for rTorrent |
| `rutorrent_hdd` | rTorrent / ruTorrent for HDD torrents |
| `vpn-deluge` | Gluetun VPN container for Deluge |
| `deluge_ssd` | Deluge for SSD downloads |
| `rtorrent-port-sync` | syncs Proton forwarded port to rTorrent |
| `deluge-port-sync` | syncs Proton forwarded port to Deluge |

## Storage layout

```text
/home/z/rutorrent-hdd       -> rTorrent config
/mnt/hdd6t/torrents         -> rTorrent downloads

/home/z/deluge-ssd          -> Deluge config
/home/z/Pobrane/Deluge-SSD  -> Deluge downloads
```

## Network isolation

rTorrent:

```yaml
network_mode: "service:vpn"
```

Deluge:

```yaml
network_mode: "service:vpn-deluge"
```

Torrent clients use the VPN containers network namespaces, so torrent traffic goes through Gluetun.

## Local web UI

| Client | URL |
|---|---|
| ruTorrent | `http://192.168.1.92:9080` |
| Deluge | `http://192.168.1.92:9082` |

## Check containers

```bash
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

## Check forwarded ports

```bash
docker exec vpn sh -c 'cat /tmp/gluetun/forwarded_port 2>/dev/null; echo'
docker exec vpn-deluge sh -c 'cat /tmp/gluetun/forwarded_port 2>/dev/null; echo'
```

## Check rTorrent port

```bash
grep -nE 'network.port_range.set|network.port_random.set' /home/z/rutorrent-hdd/rtorrent/rtorrent.rc
```

Expected:

```text
network.port_range.set = PORT-PORT
network.port_random.set = no
```

## Check Deluge port

```bash
docker exec -u abc deluge_ssd deluge-console -c /config "config listen_ports random_port"
```

Expected:

```text
listen_ports: (PORT, PORT)
random_port: False
```

## Check VPN logs

```bash
docker logs vpn --tail 80 | grep -Ei 'Connecting to|Public IP|port forwarded|error'
docker logs vpn-deluge --tail 80 | grep -Ei 'Connecting to|Public IP|port forwarded|error'
```

## Speedtest through VPN containers

```bash
docker run --rm --network container:vpn python:3.12-alpine sh -lc 'pip -q install speedtest-cli >/dev/null 2>&1 && speedtest-cli --simple --secure'
docker run --rm --network container:vpn-deluge python:3.12-alpine sh -lc 'pip -q install speedtest-cli >/dev/null 2>&1 && speedtest-cli --simple --secure'
```

## Problems solved

### VPN worked but port forwarding did not

VPN tunnel was working, speedtest worked, but `/tmp/gluetun/forwarded_port` was empty.

Conclusion:

```text
Working VPN does not automatically mean working NAT-PMP / port forwarding.
```

### rTorrent had stale port

Proton assigned a new forwarded port, but rTorrent still used an old port.

Fix:

```text
rtorrent-port-sync reads Gluetun forwarded_port and updates rtorrent.rc.
```

### Deluge port sync failed

`deluge-console` failed when executed with wrong user/config context.

Working command pattern:

```bash
docker exec -u abc deluge_ssd deluge-console -c /config "config -s random_port false"
docker exec -u abc deluge_ssd deluge-console -c /config "config -s listen_ports (PORT, PORT)"
```

## Secret safety

Never commit:

```text
.env
WireGuard private keys
Proton VPN configs
passwords
tokens
cookies
private tracker data
real private credentials
```
