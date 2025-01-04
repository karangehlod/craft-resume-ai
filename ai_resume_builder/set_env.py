import json
import os

def set_env_from_terraform_output(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {file_path}: {e}")
        return
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        return

    os.environ['AZURE_TEXT_ANALYTICS_KEY'] = data['cognitive_account_key']['value']
    os.environ['AZURE_ENDPOINT'] = data['cognitive_account_endpoint']['value']
    os.environ['AZURE_OPENAI_API_KEY'] = data['openai_account_key']['value']
    os.environ['AZURE_OPENAI_ENDPOINT'] = data['openai_account_endpoint']['value']
    os.environ['AZURE_OPENAI_ENGINE'] = data['openai_deployment_name']['value']
    os.environ['AZURE_STORAGE_CONNECTION_STRING'] = f"DefaultEndpointsProtocol=https;AccountName={data['storage_account_name']['value']};AccountKey={data['storage_account_key']['value']};EndpointSuffix=core.windows.net"
    os.environ['AZURE_TRANSLATOR_KEY'] = data['cognitive_account_key']['value']
    os.environ['AZURE_TRANSLATOR_ENDPOINT'] = data['cognitive_account_endpoint']['value']
    os.environ['AZURE_CLIENT_ID'] = 'your-azure-client-id'  # Replace with actual value
    os.environ['AZURE_CLIENT_SECRET'] = 'your-azure-client-secret'  # Replace with actual value
    os.environ['SECRET_KEY'] = 'your-secret-key'  # Replace with actual value

if __name__ == "__main__":
    set_env_from_terraform_output('terraform_output.json')