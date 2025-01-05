import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    AZURE_TEXT_ANALYTICS_KEY = os.environ.get('AZURE_TEXT_ANALYTICS_KEY')
    AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.environ.get('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_ENDPOINT = os.environ.get('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_ENGINE = os.environ.get('AZURE_OPENAI_ENGINE')
    AZURE_OPENAI_API_VERSION = os.environ.get('AZURE_OPENAI_API_VERSION')
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
    AZURE_STORAGE_CONTAINER_NAME = os.environ.get('AZURE_STORAGE_CONTAINER_NAME')
    AZURE_KEY_VAULT_URI = os.environ.get('AZURE_KEY_VAULT_URI')

config = Config()