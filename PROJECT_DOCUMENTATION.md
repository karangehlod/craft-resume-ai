# AI-Driven Resume Builder Project Documentation

## Overview

This project is an AI-driven resume builder that leverages Azure services to parse job descriptions, generate resumes, and match skills. It includes advanced features like job matching, skills gap analysis, resume formatting, real-time job insights, multi-language support, and advanced security and authentication.

## Features

- **Job Matching Algorithm**: Compares the skills from the parsed job description with the user’s existing skills.
- **Skills Gap Analysis**: Identifies any missing skills or certifications that the user might need to acquire.
- **Resume Formatting and Template Generation**: Provides users with an option to choose from different resume formats or templates.
- **Real-time Job Insights**: Integrates real-time job data from popular job boards.
- **Multi-language Support**: Uses Azure's Cognitive Services Translator to cater to users in multiple languages.
- **Advanced Security and Authentication**: Secures the API with OAuth or Azure Active Directory (AAD).
- **Rich Frontend**: A dynamic and interactive frontend built with HTML, CSS, and JavaScript.

## Prerequisites

- Python 3.8+
- Terraform
- Azure Subscription
- Azure CLI

## Project Structure

```
ai_resume_builder/
├── app/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── static/
│   ├── templates/
├── app.py
├── azure_utils.py
├── config.py
├── README.md
├── requirements.txt
├── run.py
├── set_env.py
├── terraform/
│   ├── .terraform/
│   ├── .terraform.lock.hcl
│   ├── main.tf
│   ├── outputs.tf
│   ├── variables.tf
├── terraform_output.json
├── LICENSE
├── .gitignore
├── .vscode/
│   ├── settings.json
├── venv/
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   ├── pyvenv.cfg
```

## Setup Instructions

1. **Clone the Repository**

```sh
git clone <repository-url>
cd ai_resume_builder
```

2. **Create a Virtual Environment and Activate It**

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install the Dependencies**

```sh
pip install -r requirements.txt
```

4. **Install Azure CLI**

   - **On Windows**:

     1. Download the Azure CLI Installer from the [Azure CLI installation page](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-windows?tabs=azure-cli).
     2. Run the installer and follow the instructions.
     3. Verify installation:
        ```sh
        az --version
        ```

   - **On macOS**:

     1. Install via Homebrew:
        ```sh
        brew update && brew install azure-cli
        ```
     2. Verify installation:
        ```sh
        az --version
        ```

   - **On Linux**:
     1. Follow the instructions on the [Azure CLI installation page](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-linux?pivots=apt) for your specific Linux distribution.
     2. Verify installation:
        ```sh
        az --version
        ```

5. **Authenticate with Azure CLI**

```sh
az login
```

6. **Initialize and Apply Terraform Configuration**

Navigate to the terraform directory and initialize and apply the Terraform configuration:

```sh
cd terraform
terraform init
terraform plan
terraform apply
terraform output -json > ../terraform_output.json
cd ..
```

7. **Set Environment Variables from Terraform Output**

Run the set_env.py script to set the environment variables from the Terraform output:

```sh
python set_env.py
```

8. **Run the Application**

```sh
python app.py
```

9. **Access the Application**

Open your browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Environment Variables

Ensure your `.env` file contains the following keys:

```ini
AZURE_TEXT_ANALYTICS_KEY=your-azure-text-analytics-key
AZURE_ENDPOINT=https://your-cognitive-account-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your-openai-account-key
AZURE_OPENAI_ENDPOINT=https://your-openai-account-endpoint.openai.azure.com/
AZURE_OPENAI_ENGINE=gpt-4o-mini  # or "gpt-4o" based on your preference
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your-storage-account-name;AccountKey=your-storage-account-key;EndpointSuffix=core.windows.net
AZURE_TRANSLATOR_KEY=your-cognitive-account-key
AZURE_TRANSLATOR_ENDPOINT=https://your-cognitive-account-endpoint.cognitiveservices.azure.com/
AZURE_CLIENT_ID=your-azure-client-id
AZURE_CLIENT_SECRET=your-azure-client-secret
SECRET_KEY=your-secret-key
```

## API Endpoints

- **`/login`**: Initiates the OAuth login process.
- **`/logout`**: Logs out the user by clearing the session.
- **`/login/authorized`**: Handles the OAuth callback and stores the access token in the session.
- **`/parse-job`**: Parses the job description and extracts key skills.
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "description": "Job description text"
    }
    ```
- **`/analyze-resume`**: Analyzes the resume and identifies missing skills.
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "job_description": "Job description text",
      "resume_text": "Resume text"
    }
    ```
- **`/generate-resume`**: Generates a professional resume in DOCX format.
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "user_details": "User details text",
      "job_skills": "Job skills text"
    }
    ```
- **`/upload-resume`**: Uploads the generated resume to Azure Blob Storage.
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "file_path": "Path to the resume file",
      "container_name": "Azure Blob Storage container name"
    }
    ```
- **`/translate`**: Translates the given text to the specified target language.
  - **Method**: POST
  - **Request Body**:
    ```json
    {
      "text": "Text to translate",
      "target_language": "Target language code"
    }
    ```
- **`/job-insights`**: Retrieves real-time job insights from popular job boards.
  - **Method**: GET

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

### Functionality Check

1. **Job Matching Algorithm**: Implemented in `analyze_resume` function in `app.py`.
2. **Skills Gap Analysis**: Implemented in `analyze_resume` function in `app.py`.
3. **Resume Formatting and Template Generation**: Implemented in `generate_resume_docx` function in `azure_utils.py`.
4. **Real-time Job Insights**: Placeholder function `get_job_insights` in `azure_utils.py`.
5. **Multi-language Support**: Implemented in `translate_text` function in `azure_utils.py`.
6. **Advanced Security and Authentication**: Implemented using Flask-OAuthlib in `app.py`.
7. **Rich Frontend**: Placeholder for frontend implementation.

### Missing Components

- **Real-time Job Insights**: The `get_job_insights` function needs to be implemented with actual API integration.
- **Rich Frontend**: The frontend implementation is not detailed in the current setup.

### Suggested Changes

1. Implement the `get_job_insights` function to fetch real-time job data from APIs like LinkedIn, Glassdoor, or Indeed.
2. Develop a frontend using a framework like React or Vue.js to enhance user experience.

By following these steps and suggestions, you can ensure that the AI-Driven Resume Builder project is fully functional and provides a comprehensive solution for job seekers.

---

This document provides a comprehensive overview of the AI-Driven Resume Builder project, including setup instructions, functionality explanations, and suggestions for further development. Save this document for future reference and use it as a guide for working on the project.
