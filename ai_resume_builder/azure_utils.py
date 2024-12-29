from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential
from azure.storage.blob import BlobServiceClient
from docx import Document
from dotenv import load_dotenv
import os

load_dotenv()

def authenticate_client():
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    endpoint = os.getenv("AZURE_ENDPOINT")
    return TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))

def extract_key_phrases(text):
    client = authenticate_client()
    response = client.extract_key_phrases(documents=[text])
    return response[0].key_phrases

def text_similarity(text1, text2):
    client = authenticate_client()
    documents = [{"id": "1", "text": text1}, {"id": "2", "text": text2}]
    response = client.analyze_sentiment(documents=documents)
    return response[0].confidence_scores.positive

def identify_missing_skills(job_skills, resume_skills):
    return [skill for skill in job_skills if skill not in resume_skills]

def generate_resume_docx(user_details, job_skills):
    doc = Document()
    doc.add_heading('Resume', 0)
    
    doc.add_heading('User Details', level=1)
    doc.add_paragraph(user_details)
    
    doc.add_heading('Job Skills', level=1)
    doc.add_paragraph(job_skills)
    
    doc.save('resume.docx')

def upload_to_blob(file_path, container_name):
    connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_path)
    
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data)

def translate_text(text, target_language):
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    credentials = CognitiveServicesCredentials(key)
    client = TextAnalyticsClient(endpoint=endpoint, credentials=credentials)
    
    response = client.translate(text, target_language)
    return response.translations[0].text

def get_job_insights():
    headers = {
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN',
    }
    response = requests.get('https://api.linkedin.com/v2/jobSearch', headers=headers)
    return response.json()