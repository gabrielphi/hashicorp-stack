output "public_ips" {
  description = "Endereços IPv4 públicos das VMs"
  value = {
    for name, vm in mgc_virtual_machine_instances.instances :
    name => vm.ipv4
  }
}

