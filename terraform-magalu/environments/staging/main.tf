# module "database" {
#   source = "../../modules/database"
#   name   = "test-instance"
#   user   = "dbadmin"
#   password = "examplepassword"
#   engine_name = "postgresql"
#   engine_version = "16"
#   instance_type = "BV2-4-10"
#   volume_size = 10
#   volume_type = "CLOUD_NVME15K"
#   backup_start_at = "16:00:00"
#   backup_retention_days = 1
# }
module "vm" {
  source = "../../modules/vm"
  
  providers = {
    mgc.nordeste = mgc.nordeste
  }
  
  instances = {
    "vm-1" = {
      name                = "test-vm-1"
      machine_type        = "BV2-2-20"
      image               = "cloud-ubuntu-24.04 LTS"
      allocate_public_ipv4 = true
    }
    # Adicione mais VMs conforme necessário:
    # "vm-2" = {
    #   name                = "test-vm-2"
    #   machine_type        = "BV2-2-20"
    #   image               = "cloud-ubuntu-24.04 LTS"
    #   allocate_public_ipv4 = true
    # }
  }
}

resource "local_file" "ansible_inventory" {
  filename = abspath("${path.module}/../../../ansible/inventory.ini")
  content  = templatefile("${path.module}/ansible_inventory.tpl", {
    public_ips = module.vm.public_ips
  })
}


# module "object_storage" {
#   source = "../../modules/object-storage"
#   project_name = "myproject"
#   environment  = "staging"
#   buckets = {
#     "django-media" = {
#       name       = "django-media"
#       versioning = true
#       is_public  = false  # Bucket privado - acesso restrito
#       enable_cors = false
#     }
#   }
# }