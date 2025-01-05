variable "subscription_id" {
  description = "Azure Subscription ID"
  default = "a82de6ac-27bf-4a6b-b36a-2d85e6fbcb80"
}

variable "openai_model" {
  description = "Azure OpenAI model name"
  default     = "gpt-4o-mini"  // or "gpt-4o" based on your preference
}

variable "openai_api_version" {
  description = "Azure OpenAI API version"
  default     = "2024-05-01-preview"
}

variable "location" {
  description = "Azure region"
  default     = "East US"
}