import json
import os
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def set_env_from_terraform_output(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Check if the file is empty
            content = file.read().strip()
            if not content:
                raise ValueError("The file is empty.")
            logging.info(f"File content: {content}")
            data = json.loads(content)
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='utf-16') as file:
            # Check if the file is empty
            content = file.read().strip()
            if not content:
                raise ValueError("The file is empty.")
            logging.info(f"File content: {content}")
            data = json.loads(content)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {file_path}: {e}")
        return
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}")
        return
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return

    # Define mappings for environment variables
    mappings = {
        "AZURE_TEXT_ANALYTICS_KEY": "cognitive_account_key",
        "AZURE_ENDPOINT": "cognitive_account_endpoint",
        "AZURE_OPENAI_API_KEY": "openai_account_key",
        "AZURE_OPENAI_ENDPOINT": "openai_account_endpoint",
        "AZURE_OPENAI_ENGINE": "openai_deployment_name",
        "AZURE_OPENAI_API_VERSION": "openai_api_version",
        "AZURE_STORAGE_CONNECTION_STRING": None,  # Custom logic for storage connection string
        "AZURE_STORAGE_CONTAINER_NAME": "storage_container_name",
        "AZURE_KEY_VAULT_URI": "key_vault_uri",
    }

    # Validate required keys and set environment variables
    try:
        for env_var, key in mappings.items():
            if key:
                if key not in data or "value" not in data[key]:
                    logging.error(f"Missing or malformed key in JSON: {key}")
                    return
                os.environ[env_var] = data[key]["value"]
            elif env_var == "AZURE_STORAGE_CONNECTION_STRING":
                # Build storage connection string
                storage_name = data["storage_account_name"]["value"]
                storage_key = data["storage_account_key"]["value"]
                os.environ[env_var] = (
                    f"DefaultEndpointsProtocol=https;AccountName={storage_name};"
                    f"AccountKey={storage_key};EndpointSuffix=core.windows.net"
                )

        logging.info("Environment variables set successfully.")
    except Exception as e:
        logging.error(f"Error setting environment variables: {e}")

if __name__ == "__main__":
    # Check for the file path as a command-line argument
    if len(sys.argv) < 2:
        logging.error("Usage: python set_env_from_terraform.py terraform_output.json")
        sys.exit(1)

    terraform_output_file = sys.argv[1]
    set_env_from_terraform_output(terraform_output_file)
