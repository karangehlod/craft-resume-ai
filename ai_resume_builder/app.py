import os
from flask import Flask, request, jsonify, redirect, url_for, session, send_from_directory
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import openai
from authlib.integrations.flask_client import OAuth
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(asctime)s - %(message)s")

app = Flask(__name__, static_folder='frontend/build', static_url_path='/')
app.secret_key = os.getenv("SECRET_KEY")

# Configure OpenAI
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = 'azure'
openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Configure OAuth
oauth = OAuth(app)
oauth.register(
    name='azure',
    client_id=os.getenv('AZURE_CLIENT_ID'),
    client_secret=os.getenv('AZURE_CLIENT_SECRET'),
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    authorize_params=None,
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/login/authorized',
    client_kwargs={'scope': 'openid profile email'}
)

# Azure Form Recognizer and Text Analytics credentials
form_recognizer_endpoint = os.getenv("FORM_RECOGNIZER_ENDPOINT")
form_recognizer_key = os.getenv("FORM_RECOGNIZER_KEY")
text_analytics_endpoint = os.getenv("TEXT_ANALYTICS_ENDPOINT")
text_analytics_key = os.getenv("TEXT_ANALYTICS_KEY")

form_recognizer_client = DocumentAnalysisClient(
    endpoint=form_recognizer_endpoint,
    credential=AzureKeyCredential(form_recognizer_key)
)

text_analytics_client = TextAnalyticsClient(
    endpoint=text_analytics_endpoint,
    credential=AzureKeyCredential(text_analytics_key)
)

def extract_text_from_pdf(pdf_file):
    try:
        poller = form_recognizer_client.begin_analyze_document("prebuilt-document", pdf_file)
        result = poller.result()
        text = " ".join([line.content for page in result.pages for line in page.lines])
        return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {e}")
        raise

def extract_key_phrases(text):
    # Example implementation that splits text into individual words
    # You may need to customize this based on your specific requirements
    return text.split()

def extract_key_phrases_in_batches(text, batch_size=5120):
    text_chunks = [text[i:i + batch_size] for i in range(0, len(text), batch_size)]
    key_phrases = []
    for chunk in text_chunks:
        response = text_analytics_client.extract_key_phrases(documents=[{"id": "1", "language": "en", "text": chunk}])[0]
        if hasattr(response, 'key_phrases'):
            key_phrases.extend(response.key_phrases)
    return key_phrases

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/login')
def login():
    logging.info("Initiating login process")
    redirect_uri = url_for('authorized', _external=True)
    return oauth.azure.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    logging.info("Logging out user")
    session.pop('token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    logging.info("Handling authorization response")
    token = oauth.azure.authorize_access_token()
    if token is None:
        logging.error("Access denied")
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['token'] = token
    logging.info("User authorized successfully")
    return redirect(url_for('index'))

@app.route('/parse-job', methods=['POST'])
def parse_job():
    description = request.json.get('description')
    logging.info(f"Parsing job description: {description}")
    result = extract_key_phrases(description)
    return jsonify(result)

@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    job_description = request.form.get('job_description')
    resume_file = request.files.get('resume_file')
    resume_text = request.form.get('resume_text')

    if not job_description:
        return jsonify({"error": "Job description is required"}), 400

    if resume_file:
        try:
            resume_text = extract_text_from_pdf(resume_file)
        except UnicodeDecodeError:
            return jsonify({"error": "Failed to decode resume file"}), 400

    if not resume_text:
        return jsonify({"error": "Resume text or file is required"}), 400

    job_skills = extract_key_phrases(job_description)
    try:
        resume_skills = extract_key_phrases_in_batches(resume_text)
    except AttributeError as e:
        if "DocumentError" in str(e):
            return jsonify({"error": "Document too large to be processed. Please limit document size to 5120 text elements."}), 400
        else:
            raise

    logging.info(f"Job skills: {job_skills}")
    logging.info(f"Resume skills: {resume_skills}")

    job_skills_set = set(job_skills)
    resume_skills_set = set(resume_skills)

    missing_skills = list(job_skills_set - resume_skills_set)
    score = (len(job_skills_set - resume_skills_set) / len(job_skills_set)) * 100
    suggested_keywords = missing_skills

    logging.info(f"Missing skills: {missing_skills}")
    logging.info(f"Score: {score}")
    logging.info(f"Suggested keywords: {suggested_keywords}")

    return jsonify({"missing_skills": missing_skills, "score": score, "suggested_keywords": suggested_keywords})

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    user_details = request.json.get('user_details')
    job_skills = request.json.get('job_skills')
    logging.info(f"Generating resume for user details: {user_details} and job skills: {job_skills}")
    result = generate_resume_docx(user_details, job_skills)
    return jsonify(result)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file_path = request.json.get('file_path')
    container_name = request.json.get('container_name')
    logging.info(f"Uploading resume from file path: {file_path} to container: {container_name}")
    result = upload_to_blob(file_path, container_name)
    return jsonify(result)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json.get('text')
    target_language = request.json.get('target_language')
    logging.info(f"Translating text: {text} to language: {target_language}")
    result = translate_text(text, target_language)
    return jsonify(result)

@app.route('/job_insights', methods=['GET'])
def job_insights():
    logging.info("Fetching job insights")
    result = get_job_insights()
    return jsonify(result)

if __name__ == '__main__':
    logging.info("Starting Flask application")
    app.run(debug=True)