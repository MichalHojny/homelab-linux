output "backend_vm" {
  description = "Backend VM connection info"
  value = {
    name = var.backend_vm_name
    ip   = var.backend_ip
    ssh  = "ssh ${var.vm_user}@${var.backend_ip}"
  }
}

output "frontend_vm" {
  description = "Frontend VM connection info"
  value = {
    name = var.frontend_vm_name
    ip   = var.frontend_ip
    ssh  = "ssh ${var.vm_user}@${var.frontend_ip}"
  }
}

output "ansible_test_inventory_hint" {
  description = "Temporary inventory lines for testing Terraform-created VMs"
  value       = <<EOT
[backend_tf]
${var.backend_vm_name} ansible_host=${var.backend_ip} ansible_user=${var.vm_user}

[frontend_tf]
${var.frontend_vm_name} ansible_host=${var.frontend_ip} ansible_user=${var.vm_user}

[company_lab_tf:children]
backend_tf
frontend_tf
EOT
}
