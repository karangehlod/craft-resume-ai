# AI-Driven Resume Builder

## Overview

This project is an AI-driven resume builder that uses Azure services to parse job descriptions, generate resumes, and match skills. It includes advanced features like job matching, skills gap analysis, resume formatting, real-time job insights, multi-language support, and advanced security and authentication.

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

## Project Structure

```
ai_resume_builder/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── forms.py
│   ├── models.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── result.html
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   ├── js/
│   │   │   └── scripts.js
├── config.py
├── run.py
├── requirements.txt
├── README.md
├── app.py
├── azure_utils.py
├── .env
├── set_env.py
├── terraform/
│   ├── main.tf
│   ├── variables.tf
│   ├── outputs.tf
└── venv/
```

## Setup Instructions

### Step 1: Clone the Repository

```sh
git clone <repository-url>
cd ai_resume_builder
```

### Step 2: Create a Virtual Environment and Activate It

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install the Dependencies

```sh
pip install -r requirements.txt
```

### Step 4: Initialize and Apply Terraform Configuration

Navigate to the terraform directory and initialize and apply the Terraform configuration:

```sh
cd terraform
terraform init
terraform apply
terraform output -json > ../terraform_output.json
cd ..
```

### Step 5: Set Environment Variables from Terraform Output

Run the set_env.py script to set the environment variables from the Terraform output:

```sh
python set_env.py
```

### Step 6: Run the Application

```sh
python app.py
```

### Step 7: Access the Application

Open your browser and go to http://127.0.0.1:5000/.

## Environment Variables

Ensure your .env file contains the following keys:

```
AZURE_TEXT_ANALYTICS_KEY=your-azure-text-analytics-key
AZURE_ENDPOINT=https://your-cognitive-account-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your-openai-account-key
AZURE_OPENAI_ENDPOINT=https://your-openai-account-endpoint.openai.azure.com/
AZURE_OPENAI_ENGINE=davinci
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=your-storage-account-name;AccountKey=your-storage-account-key;EndpointSuffix=core.windows.net
AZURE_TRANSLATOR_KEY=your-cognitive-account-key
AZURE_TRANSLATOR_ENDPOINT=https://your-cognitive-account-endpoint.cognitiveservices.azure.com/
AZURE_CLIENT_ID=your-azure-client-id
AZURE_CLIENT_SECRET=your-azure-client-secret
SECRET_KEY=your-secret-key
```

## Usage

### Parsing Job Descriptions

Send a POST request to `/parse-job` with the job description in the request body to extract key skills.

### Analyzing Resumes

Send a POST request to `/analyze-resume` with the job description and resume text in the request body to analyze the resume and identify missing skills.

### Generating Resumes

Send a POST request to `/generate-resume` with user details and job skills in the request body to generate a professional resume.

### Uploading Resumes

Send a POST request to `/upload-resume` with the file path and container name in the request body to upload the resume to Azure Blob Storage.

### Translating Text

Send a POST request to `/translate` with the text and target language in the request body to translate the text.

### Getting Job Insights

Send a GET request to `/job-insights` to get real-time job insights from popular job boards.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

