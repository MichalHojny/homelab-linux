# Homelab Linux

Personal Linux homelab focused on system administration, networking, virtualization, secure remote access, reverse proxying, automation, monitoring and infrastructure troubleshooting.

This repository documents a small but realistic lab environment built on an Arch Linux host. The goal is to learn Linux administration through real services, real network problems, repeatable automation and real recovery procedures.

## Project goals

- Learn Linux administration through practical infrastructure work.
- Keep public ports closed whenever possible.
- Use Cloudflare Tunnel as the external entry point.
- Route HTTP services through a local nginx reverse proxy.
- Separate services using VMs and containers.
- Automate VM provisioning with Terraform.
- Automate service configuration with Ansible.
- Document configuration, troubleshooting, rollback and restore steps.
- Build a portfolio-quality homelab that can be explained during job interviews.
- Keep secrets, tokens, passwords and private environment files out of Git.

## Current stack

| Area | Technology |
|---|---|
| Host OS | Arch Linux |
| Virtualization | KVM / libvirt |
| Infrastructure as Code | Terraform with libvirt provider |
| Provisioning | cloud-init |
| Configuration management | Ansible |
| VM images | Ubuntu cloud images, Debian, BlackArch, Whonix |
| Containers | Docker / Docker Compose |
| Reverse proxy | nginx |
| Remote access | Apache Guacamole |
| External access | Cloudflare Tunnel |
| Firewall | UFW |
| Monitoring | Prometheus, Grafana, node-exporter, cAdvisor |
| Logging | Loki, Promtail |
| Documentation | Git / GitHub |

## High-level architecture

External traffic is routed through Cloudflare Tunnel into the Arch host. The host uses nginx as a local reverse proxy and routes traffic to internal services, VMs and containers.

```text
Internet
   |
   v
Cloudflare Tunnel
   |
   v
Arch Linux host
   |
   +--> nginx reverse proxy
   |
   +--> Docker services
   |      +--> Guacamole
   |      +--> monitoring stack
   |
   +--> KVM/libvirt VMs
          +--> srv-01 / srv-01-tf backend
          +--> srv-02 / srv-02-tf frontend
          +--> BlackArch lab VM
          +--> Whonix Gateway
```

## Network map

| Component | Address / Network | Role |
|---|---:|---|
| Home router | `192.168.1.1` | LAN gateway |
| Arch host | `192.168.1.92` | Main host / hypervisor |
| libvirt bridge | `192.168.122.1/24` | VM gateway and DNS |
| Manual backend VM | `192.168.122.10` | `srv-01` backend/API |
| Manual frontend VM | `192.168.122.50` | `srv-02` frontend/nginx |
| Terraform backend VM | `192.168.122.11` | `srv-01-tf` backend/API |
| Terraform frontend VM | `192.168.122.51` | `srv-02-tf` frontend/nginx |
| Docker default bridge | `172.17.0.1/16` | Default Docker network |
| Guacamole network | `172.19.0.0/16` | Guacamole / guacd network |
| Host xrdp | `192.168.1.92:3389` | Remote desktop target |
| Ollama | `127.0.0.1:11434` | Local AI service |
| ruTorrent | `192.168.1.92:9080` | Historical local torrent UI |

## Virtual machines

### Manual lab VMs

| VM | OS | IP | Role |
|---|---|---:|---|
| `srv-01` | Ubuntu | `192.168.122.10` | Backend/API server |
| `srv-02` | Debian | `192.168.122.50` | Frontend/nginx server |

### Terraform-managed lab VMs

Terraform creates two Ubuntu cloud-image based VMs for repeatable infrastructure testing.

| VM | IP | CPU | RAM | Disk | Role |
|---|---:|---:|---:|---:|---|
| `srv-01-tf` | `192.168.122.11` | 1 vCPU | 1536 MB | 20 GB qcow2 | Backend/API server |
| `srv-02-tf` | `192.168.122.51` | 1 vCPU | 1536 MB | 20 GB qcow2 | Frontend/nginx server |

Terraform VM provisioning includes:

- Ubuntu Noble cloud image.
- Thin qcow2 disks based on a reusable base image.
- cloud-init user-data and network-data.
- Static IP addresses.
- `ansible` SSH user.
- SSH key injection.
- libvirt default NAT network.
- ACPI/APIC enabled for proper Ubuntu cloud-image boot.
- Tested `terraform apply` and `terraform destroy` workflow.

### BlackArch

| Item | Value |
|---|---|
| VM name | `blackarch` |
| Storage | Encrypted host partition |
| Role | Security tools lab |
| Intended routing | Through Whonix Gateway |

BlackArch is intended for controlled security learning inside the local lab only.

### Whonix Gateway

| Item | Value |
|---|---|
| VM name | `Whonix-Gateway` |
| Role | Tor gateway for isolated testing |
| Planned use | BlackArch traffic routed through Whonix |

## Main projects

### company-lab

A small production-like two-server web application.

Architecture:

- Browser connects to the frontend server.
- Frontend server serves static files through nginx.
- nginx proxies API requests to the backend server.
- Backend server runs a FastAPI application as a systemd service.
- SQLite is used as a small local database.

Main components:

| Component | Path |
|---|---|
| Backend app | `homelab/ansible/files/backend/app.py` |
| Backend database init | `homelab/ansible/files/backend/init_db.py` |
| Backend requirements | `homelab/ansible/files/backend/requirements.txt` |
| Frontend files | `homelab/ansible/files/frontend/` |
| systemd service | `homelab/ansible/files/systemd/company-backend.service` |
| Ansible playbook | `homelab/ansible/site.yml` |

### Terraform libvirt lab

Terraform project path:

```text
homelab/terraform/libvirt-company-lab
```

Main files:

| File | Purpose |
|---|---|
| `main.tf` | libvirt volumes, cloud-init disks and VM definitions |
| `variables.tf` | VM names, IP addresses, image path and storage pool settings |
| `outputs.tf` | SSH and Ansible inventory hints |
| `cloud-init/user-data.yml.tftpl` | user, SSH key and package setup |
| `cloud-init/network-config.yml.tftpl` | static network configuration |
| `.terraform.lock.hcl` | provider lock file |

Basic workflow:

```bash
cd homelab/terraform/libvirt-company-lab
terraform init
terraform validate
terraform apply
```

Destroy test infrastructure:

```bash
cd homelab/terraform/libvirt-company-lab
terraform destroy
```

Important notes:

- Run Terraform commands from `homelab/terraform/libvirt-company-lab`.
- Do not run `terraform destroy` from the Ansible directory.
- `terraform.tfstate`, `.terraform/`, `tfplan`, VM images and ISO files must not be committed.
- Terraform local state is intentionally kept local and ignored by Git.

### Ansible automation

Ansible project path:

```text
homelab/ansible
```

Important files:

| File | Purpose |
|---|---|
| `inventory.ini` | Manual VM inventory |
| `inventory-tf.ini` | Terraform-created VM inventory |
| `site.yml` | Main deployment playbook |
| `ansible.cfg` | Local Ansible configuration |
| `files/backend/` | Backend application files |
| `files/frontend/` | Frontend static files |
| `files/systemd/` | systemd service files |

Test connectivity:

```bash
cd homelab/ansible
ansible -i inventory-tf.ini company_lab -m ping
```

Deploy to Terraform-created VMs:

```bash
cd homelab/ansible
ansible-playbook -i inventory-tf.ini site.yml
```

Dry-run check:

```bash
cd homelab/ansible
ansible-playbook -i inventory-tf.ini site.yml --check --diff
```

Note: some tasks that depend on newly created directories may not be fully check-mode friendly on a fresh VM.

### guacamole

Apache Guacamole setup for browser-based remote access.

Current role:

- Browser-based remote access to internal systems.
- guacd connects to host xrdp.
- External access is intended to go through Cloudflare Tunnel and local nginx.
- Direct public port forwarding should be avoided.

Security notes:

- Real `.env` files are ignored.
- `.env.example` files use placeholders only.
- Real database passwords must never be committed.

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

### monitoring

Monitoring and logging stack based on Docker Compose.

Components:

| Component | Role |
|---|---|
| Prometheus | Metrics collection |
| Grafana | Dashboards |
| node-exporter | Host metrics |
| cAdvisor | Container metrics |
| Loki | Log storage |
| Promtail | Log shipping |

Secrets are configured through local `.env` files and committed only as `.env.example` placeholders.

## Known working workflow

The current working infrastructure workflow is:

```text
Terraform creates VMs
        |
        v
cloud-init configures users, SSH and static IPs
        |
        v
Ansible connects over SSH
        |
        v
Ansible installs packages and deploys backend/frontend
        |
        v
Services are checked with curl, systemctl and Ansible commands
```

Working test targets:

| VM | IP | Test |
|---|---:|---|
| `srv-01-tf` | `192.168.122.11` | SSH, cloud-init, backend deployment |
| `srv-02-tf` | `192.168.122.51` | SSH, cloud-init, frontend/nginx deployment |

## Operational checks

| Area | Command |
|---|---|
| Hostname | `hostname` |
| IP addresses | `ip -br a` |
| Routing | `ip route` |
| Listening ports | `ss -tulpn` |
| Failed services | `systemctl --failed` |
| VMs | `virsh -c qemu:///system list --all` |
| VM interfaces | `virsh -c qemu:///system domiflist <vm-name>` |
| libvirt networks | `virsh -c qemu:///system net-list --all` |
| libvirt DHCP leases | `virsh -c qemu:///system net-dhcp-leases default` |
| Docker containers | `docker ps` |
| Docker networks | `docker network ls` |
| nginx config test | `sudo nginx -t` |
| nginx status | `systemctl status nginx --no-pager` |
| UFW rules | `sudo ufw status numbered` |
| Backend status | `systemctl status company-backend --no-pager` |
| Backend health | `curl -s http://192.168.122.11:3000/health` |
| Frontend check | `curl -I http://192.168.122.51` |
| Ansible ping | `ansible -i inventory-tf.ini company_lab -m ping` |
| Terraform state | `terraform state list` |

## Troubleshooting notes

### Terraform VM exists but SSH does not work

Useful checks:

```bash
cd homelab/terraform/libvirt-company-lab
terraform state list
virsh -c qemu:///system list --all
ip route get 192.168.122.11
virsh -c qemu:///system domiflist srv-01-tf
sudo tail -n 120 /var/log/libvirt/qemu/srv-01-tf.log
```

Important lessons learned:

- A VM can exist in libvirt but still fail to boot properly.
- Terraform state tells what Terraform manages.
- QEMU logs can reveal VM boot options.
- Ubuntu cloud images need a correct VM definition.
- ACPI/APIC settings were important for proper booting in this lab.
- A blank virt-manager screen does not always mean the VM has no disk or no OS.

### Terraform state

Terraform commands must be run from the directory that contains the Terraform project and local state:

```text
homelab/terraform/libvirt-company-lab
```

Running `terraform destroy` from another directory, such as `homelab/ansible`, will not destroy the libvirt VMs managed by this Terraform project.

### Git safety checks

Before committing, check staged files:

```bash
git diff --cached --name-only
```

Check for unwanted files in stage:

```bash
git diff --cached --name-only | grep -Ei 'tfstate|tfplan|\.terraform|qcow2|iso|img|backup|\.env' || echo "OK: no local artifacts staged"
```

Case-insensitive secret scan for staged files:

```bash
git diff --cached --name-only | xargs -r grep -nIiE 'password|passwd|pwd|token|secret|credential|credentials|private key|begin rsa|begin openssh|api[_-]?key|client[_-]?secret|cloudflare'
```

For safer local audits, first list matching files instead of printing secret values:

```bash
grep -RIlEi --exclude-dir=.git --exclude-dir=.terraform --exclude='terraform.tfstate*' --exclude='tfplan' --exclude='*.plan' --exclude='*.backup.*' --exclude='*.bak' 'password|passwd|pwd|token|secret|credential|credentials|private key|begin rsa|begin openssh|api[_-]?key|client[_-]?secret|cloudflare' .
```

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
11. Prefer repeatable automation over undocumented manual changes.
12. Use one change, one test, one conclusion.

## Current status

Implemented:

- Arch Linux host with KVM/libvirt.
- Default libvirt NAT network.
- Ubuntu and Debian manual VMs.
- Terraform-managed Ubuntu cloud-image VMs.
- cloud-init based VM provisioning.
- Static IP configuration for Terraform VMs.
- Ansible user access to manual and Terraform VMs.
- Ansible deployment for company-lab backend/frontend.
- VM DNS troubleshooting through libvirt dnsmasq.
- UFW rules for VM DNS access.
- Apache Guacamole remote access stack.
- Basic nginx reverse proxy structure.
- Monitoring and logging stack.
- GitHub documentation and infrastructure config tracking.

In progress:

- Cleaner project documentation.
- Better deployment and rollback documentation.
- Backup and restore procedure.
- Service hardening.
- Whonix and BlackArch isolation workflow.
- VPN before Tor testing for isolated lab traffic.

## Roadmap

### High priority

- Improve company-lab documentation.
- Add clearer rollback steps for Terraform and Ansible.
- Add backup and restore documentation.
- Add Terraform README inside `homelab/terraform/libvirt-company-lab`.
- Add Ansible README inside `homelab/ansible`.

### Medium priority

- Improve monitoring dashboards.
- Add architecture diagrams.
- Improve Fail2ban rules.
- Add security audit checklist.
- Add GitHub Actions validation for shell, YAML, Ansible and Terraform.

### Later

- Add Docker service template.
- Add Kubernetes/k3s lab after nginx, systemd and Ansible are solid.
- Add AI infrastructure lab using Ollama or vLLM when host resources allow it.
- Add separate I2P/Hyphanet privacy lab VMs for controlled experiments.

## Learning focus

This homelab is aimed at building practical skills for:

- Linux administration
- networking and DNS troubleshooting
- KVM/libvirt virtualization
- Terraform infrastructure automation
- cloud-init provisioning
- Ansible configuration management
- Docker and service separation
- nginx reverse proxying
- secure remote access
- firewalling and hardening
- monitoring and logging
- backup and disaster recovery
- DevOps and future AI infrastructure work
