# DNS Troubleshooting (VMs)

## Symptoms

- ping 192.168.122.1 works
- ping 9.9.9.9 works
- ping google.com fails

## Meaning

- network OK
- internet OK
- DNS broken

## Root cause

UFW on host blocked DNS traffic from VM network.

## Fix

sudo ufw allow in on virbr0 to 192.168.122.1 port 53 proto udp
sudo ufw allow in on virbr0 to 192.168.122.1 port 53 proto tcp

## Ubuntu issue

systemd-resolved was correct, but /etc/resolv.conf was wrong.

Fix:

sudo rm -f /etc/resolv.conf
sudo ln -s /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

## Key lesson

IP connectivity ≠ DNS resolution
