variable "libvirt_uri" {
  description = "Libvirt connection URI"
  type        = string
  default     = "qemu:///system"
}

variable "storage_pool" {
  description = "Libvirt storage pool for VM disks"
  type        = string
  default     = "vm-lab"
}

variable "network_name" {
  description = "Libvirt network name"
  type        = string
  default     = "default"
}

variable "ubuntu_cloud_image" {
  description = "Path to Ubuntu 24.04 cloud image"
  type        = string
  default     = "/home/z/vm-lab/cloud-images/noble-server-cloudimg-amd64.img"
}

variable "ssh_public_key_path" {
  description = "SSH public key injected into VMs by cloud-init"
  type        = string
  default     = "/home/z/.ssh/id_ed25519.pub"
}

variable "vm_user" {
  description = "Default user created by cloud-init"
  type        = string
  default     = "ansible"
}

variable "backend_vm_name" {
  description = "Backend VM name"
  type        = string
  default     = "srv-01-tf"
}

variable "frontend_vm_name" {
  description = "Frontend VM name"
  type        = string
  default     = "srv-02-tf"
}

variable "backend_ip" {
  description = "Static IP for backend VM"
  type        = string
  default     = "192.168.122.11"
}

variable "frontend_ip" {
  description = "Static IP for frontend VM"
  type        = string
  default     = "192.168.122.51"
}

variable "gateway" {
  description = "Default gateway for libvirt NAT network"
  type        = string
  default     = "192.168.122.1"
}

variable "dns_server" {
  description = "DNS server for VMs"
  type        = string
  default     = "192.168.122.1"
}
