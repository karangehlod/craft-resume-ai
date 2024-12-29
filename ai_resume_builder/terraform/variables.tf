variable "subscription_id" {
  description = "Azure Subscription ID"
}

variable "openai_model" {
  description = "Azure OpenAI model name"
  default     = "gpt-4o-mini"  // or "gpt-4o" based on your preference
}

variable "openai_api_version" {
  description = "Azure OpenAI API version"
  default     = "2023-05-15"
}

variable "location" {
  description = "Azure region"
  default     = "East US"
}