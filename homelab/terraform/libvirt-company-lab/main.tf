terraform {
  required_version = ">= 1.5.0"

  required_providers {
    libvirt = {
      source  = "dmacvicar/libvirt"
      version = "~> 0.9.0"
    }
  }
}

provider "libvirt" {
  uri = var.libvirt_uri
}

locals {
  ssh_public_key = trimspace(file(var.ssh_public_key_path))

  vms = {
    backend = {
      name   = var.backend_vm_name
      ip     = var.backend_ip
      memory = 1536
      vcpu   = 1
      role   = "backend"
    }

    frontend = {
      name   = var.frontend_vm_name
      ip     = var.frontend_ip
      memory = 1536
      vcpu   = 1
      role   = "frontend"
    }
  }
}

resource "libvirt_volume" "ubuntu_base" {
  name = "ubuntu-noble-base.qcow2"
  pool = var.storage_pool

  create = {
    content = {
      url = "file://${var.ubuntu_cloud_image}"
    }
  }

  target = {
    format = {
      type = "qcow2"
    }
  }
}

resource "libvirt_volume" "vm_disk" {
  for_each = local.vms

  name     = "${each.value.name}.qcow2"
  pool     = var.storage_pool
  capacity = 21474836480

  backing_store = {
    path = libvirt_volume.ubuntu_base.path
    format = {
      type = "qcow2"
    }
  }

  target = {
    format = {
      type = "qcow2"
    }
  }
}

resource "libvirt_cloudinit_disk" "cloudinit" {
  for_each = local.vms

  name = "${each.value.name}-cloudinit.iso"

  meta_data = yamlencode({
    instance-id    = each.value.name
    local-hostname = each.value.name
  })

  user_data = templatefile("${path.module}/cloud-init/user-data.yml.tftpl", {
    hostname       = each.value.name
    vm_user        = var.vm_user
    ssh_public_key = local.ssh_public_key
  })

  network_config = templatefile("${path.module}/cloud-init/network-config.yml.tftpl", {
    ip_address = each.value.ip
    gateway    = var.gateway
    dns_server = var.dns_server
  })
}

resource "libvirt_domain" "vm" {
  for_each = local.vms

  name        = each.value.name
  type        = "kvm"
  memory      = each.value.memory
  memory_unit = "MiB"
  vcpu        = each.value.vcpu
  autostart   = false
  running     = true

  features = {
    acpi = true
    apic = {}
  }

  os = {
    type         = "hvm"
    type_arch    = "x86_64"
    type_machine = "q35"
    boot_devices = [{ dev = "hd" }]
  }

  devices = {
    disks = [
      {
        source = {
          file = {
            file = libvirt_volume.vm_disk[each.key].path
          }
        }

        target = {
          dev = "vda"
          bus = "virtio"
        }

        driver = {
          name = "qemu"
          type = "qcow2"
        }
      },
      {
        source = {
          file = {
            file = libvirt_cloudinit_disk.cloudinit[each.key].path
          }
        }

        target = {
          dev = "sda"
          bus = "sata"
        }

        readonly = true
      }
    ]

    interfaces = [
      {
        model = {
          type = "virtio"
        }

        source = {
          network = {
            network = var.network_name
          }
        }
      }
    ]

    serials = [
      {
        type = "pty"

        target = {
          type = "isa-serial"
          port = 0
        }
      }
    ]

    consoles = [
      {
        type = "pty"

        target = {
          type = "serial"
          port = 0
        }
      }
  ] }
}
