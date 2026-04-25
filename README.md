# Homelab Linux

My personal Linux homelab project.

## Stack

- Arch Linux
- Nginx reverse proxy
- Guacamole remote access
- Docker Compose
- Cloudflare DNS / WAF / Geo-block
- UFW firewall
- Fail2ban
- ruTorrent local access

## Current architecture

Internet -> Cloudflare -> Nginx HTTP Auth -> Guacamole -> SSH to host

## Security

- Cloudflare geo-block
- HTTP Basic Auth
- Guacamole authentication
- UFW firewall
- Guacamole exposed only on localhost
- SSH access via Guacamole

## TODO

- Finish Fail2ban nginx jail
- Add Nginx rate limiting
- Add VM lab
- Document backup/restore procedure
