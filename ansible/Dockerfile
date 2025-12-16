FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      openssh-client \
      sshpass \
      git \
      ca-certificates && \
    pip install --no-cache-dir ansible && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/ansible

# Copiar ansible.cfg para dentro da imagem (não como volume para evitar problemas de permissão)
COPY ansible.cfg /etc/ansible/ansible.cfg

# Copiar e configurar script de entrypoint
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]


