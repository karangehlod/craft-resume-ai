from app import create_app
import logging
import os
import sys
from set_env import set_env_from_terraform_output

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set environment variables from terraform_output.json
terraform_output_file = 'terraform_output.json'
set_env_from_terraform_output(terraform_output_file)

app = create_app()

if __name__ == "__main__":
    logging.info("Starting the application")
    app.run(debug=True)