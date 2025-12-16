[hashicorp_nodes]
%{ for name, ip in public_ips ~}
${name} ansible_host=${ip} ansible_user=ubuntu ansible_ssh_private_key_file=/root/.ssh/id_ed25519
%{ endfor ~}


