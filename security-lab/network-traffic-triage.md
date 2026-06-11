# Network traffic triage basics

Goal: practice basic network checks useful for Support, NOC and SOC L1 work.

## Check listening ports

```bash
sudo ss -tulpn

Useful columns:

ColumnMeaning
Netidtcp/udp
Local Address:Portlistening address and port
Processprocess using the port
Check active connections
ss -tunap

Filter established connections:

ss -tunap | grep ESTAB
Check default route
ip route

Expected default route example:

default via 192.168.1.1 dev enp3s0
Check DNS resolution
dig example.com
resolvectl status
Check HTTP response
curl -I http://example.com
curl -v https://example.com
Capture traffic with tcpdump

Capture DNS:

sudo tcpdump -nn -i enp3s0 port 53

Capture HTTP/HTTPS to one host:

sudo tcpdump -nn -i enp3s0 host 1.1.1.1

Capture SSH:

sudo tcpdump -nn -i enp3s0 port 22
What to look for
SymptomPossible cause
DNS fails, ping to IP worksDNS problem
No default routerouting problem
Port not listeningservice down or wrong config
Connection refusedhost reachable, service closed
Timeoutfirewall/routing/service not responding
Many failed SSH attemptsscanning or brute force
Unexpected outbound connectionneeds investigation
Basic triage flow
1. Is the host online?
2. Does it have IP address?
3. Does it have default route?
4. Does DNS work?
5. Is the service listening?
6. Is firewall blocking it?
7. What do logs say?
8. Can I reproduce with curl/dig/ss/tcpdump?

