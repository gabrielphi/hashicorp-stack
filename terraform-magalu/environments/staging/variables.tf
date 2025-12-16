variable "api_key" {
  type        = string
  sensitive   = true
  description = "The Magalu Cloud API Key"
  default     = "c56d2787-add8-45ed-a3cf-3a2dca260566"
}

variable "mgc_key_pair_id" {
  type        = string
  sensitive   = true
  description = "The Magalu Cloud key pair id"
  default     = "944542b2-2e7d-4157-9550-ad10ae2be52b"
}

variable "mgc_key_pair_secret" { 
    type        = string
    sensitive   = true
    description = "The Magalu Cloud key pair secret"
    default     = "9106239d-2f4a-4076-b6a7-8b763e4ab311"
}

variable "region" {
    type        = string
    description = "The Magalu Cloud region"
    default     = "br-se1"
}

