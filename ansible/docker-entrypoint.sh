#!/bin/bash
set -e

# Desabilitar ssh-agent completamente
unset SSH_AUTH_SOCK
unset SSH_AGENT_PID
export SSH_AUTH_SOCK=""

# Criar diretório .ssh se não existir
mkdir -p /root/.ssh
chmod 700 /root/.ssh

# A chave é montada como /root/.ssh/id_ed25519 (definido no docker-compose)
# Ajustar permissões para 0600 (SSH requer permissões restritas)
if [ -f /root/.ssh/id_ed25519 ]; then
    echo "Chave SSH encontrada: /root/.ssh/id_ed25519"
    ls -la /root/.ssh/id_ed25519
    
    # Ajustar permissões para 0600 (SSH requer permissões restritas)
    chmod 600 /root/.ssh/id_ed25519
    
    echo "Permissões da chave ajustadas:"
    ls -la /root/.ssh/id_ed25519
else
    echo "ERRO: Chave SSH /root/.ssh/id_ed25519 não encontrada!"
    echo "Verifique se a chave está configurada corretamente no docker-compose.yml"
    exit 1
fi

# Verificar se o ansible.cfg está sendo usado
if [ -f /etc/ansible/ansible.cfg ]; then
    echo "Usando ansible.cfg de: /etc/ansible/ansible.cfg"
fi

# Executar o comando passado
exec "$@"

