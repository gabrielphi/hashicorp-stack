output "vm_public_ips" {
  description = "Mapa de IPs públicos das VMs criadas"
  value       = module.vm.public_ips
}

