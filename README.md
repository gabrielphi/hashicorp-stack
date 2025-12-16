# HashiCorp Stack - Consul + Nomad

Stack completa para provisionar Consul e Nomad em VMs Ubuntu 24.04 usando Terraform + Ansible.

## Pré-requisitos

- Terraform instalado
- Docker Desktop instalado e rodando (para executar Ansible via container)
- Chave SSH configurada na Magalu Cloud
- Credenciais da Magalu Cloud configuradas

## Fluxo de Trabalho

### 1. Provisionar VMs com Terraform

Primeiro, você precisa criar as VMs e gerar o inventário do Ansible:

```powershell
cd terraform-magalu/environments/staging
terraform init
terraform plan
terraform apply
```

O Terraform irá:
- Criar as VMs na Magalu Cloud
- Gerar automaticamente o arquivo `ansible/inventory.ini` com os IPs públicos

### 2. Executar Ansible via Docker

Após o Terraform criar as VMs e gerar o inventário, execute o Ansible:

```powershell
# Na raiz do projeto
docker compose up --build
```

Ou para executar interativamente:

```powershell
docker compose run --rm ansible bash
# Dentro do container:
ansible-playbook -i inventory.ini site.yml
```

## Estrutura do Projeto

```
hashicorp-stack/
├── ansible/
│   ├── Dockerfile              # Imagem Docker com Ansible
│   ├── inventory.ini           # Gerado automaticamente pelo Terraform
│   ├── site.yml                # Playbook principal
│   └── roles/
│       └── hashicorp_nomad_consul/
│           ├── tasks/          # Tasks de instalação e configuração
│           ├── templates/      # Templates de configuração
│           └── handlers/       # Handlers para restart de serviços
├── terraform-magalu/
│   ├── modules/vm/             # Módulo para criar VMs
│   └── environments/staging/   # Ambiente de staging
│       ├── main.tf             # Configuração principal
│       └── ansible_inventory.tpl # Template para gerar inventory.ini
└── docker-compose.yml          # Docker Compose para Ansible
```

## Configuração

### Chave SSH

O Ansible usa autenticação por chave SSH. Certifique-se de que:

1. A chave pública está configurada no Terraform (`terraform-magalu/modules/vm/main.tf`)
2. A chave privada correspondente está em `~/.ssh/id_rsa` (ou defina `ANSIBLE_PRIVATE_KEY`)

### Variáveis do Terraform

Configure as variáveis necessárias em `terraform-magalu/environments/staging/variables.tf`:

- `api_key`: Chave de API da Magalu Cloud
- `region`: Região (ex: `br-ne1`)
- `mgc_key_pair_id` e `mgc_key_pair_secret`: Credenciais da Magalu Cloud

## Troubleshooting

### Erro: "provided hosts list is empty"

Isso significa que o `ansible/inventory.ini` está vazio. Execute o Terraform primeiro:

```powershell
cd terraform-magalu/environments/staging
terraform apply
```

### Erro: "Docker Engine not found"

Certifique-se de que o Docker Desktop está instalado e rodando no Windows.

### Erro de conexão SSH

Verifique:
- A chave SSH está correta no Terraform
- A chave privada está em `~/.ssh/id_rsa` (ou ajuste `ANSIBLE_PRIVATE_KEY`)
- O Security Group da VM permite conexões SSH (porta 22)
