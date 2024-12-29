from flask import Flask, request, jsonify, redirect, url_for, session
from azure_utils import extract_key_phrases, identify_missing_skills, generate_resume_docx, upload_to_blob, translate_text, text_similarity
from dotenv import load_dotenv
import openai
import os
from flask_oauthlib.client import OAuth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = 'azure'
openai.api_version = '2022-12-01'

oauth = OAuth(app)
azure = oauth.remote_app(
    'azure',
    consumer_key=os.getenv('AZURE_CLIENT_ID'),
    consumer_secret=os.getenv('AZURE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://graph.microsoft.com/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/token',
    authorize_url='https://login.microsoftonline.com/YOUR_TENANT_ID/oauth2/v2.0/authorize'
)

@app.route('/login')
def login():
    return azure.authorize(callback=url_for('authorized', _external=True))

@app.route('/logout')
def logout():
    session.pop('azure_token')
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    response = azure.authorized_response()
    if response is None or response.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['azure_token'] = (response['access_token'], '')
    return redirect(url_for('index'))

@azure.tokengetter
def get_azure_oauth_token():
    return session.get('azure_token')

def generate_resume_text(user_details, job_skills):
    prompt = f"Generate a professional resume for the following user details: {user_details} and job skills: {job_skills}."
    response = openai.Completion.create(
        engine=os.getenv("AZURE_OPENAI_ENGINE"),
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

def analyze_resume(job_description, resume_text):
    job_skills = extract_key_phrases(job_description)
    resume_skills = extract_key_phrases(resume_text)
    
    # Identify missing skills
    missing_skills = identify_missing_skills(job_skills, resume_skills)
    
    if not missing_skills:
        return "Your resume is perfect for the job."
    
    # Generate updated resume sections
    similarity_score = text_similarity(job_description, resume_text)
    prompt = f"Update the following resume sections based on the job description: {job_description}. Resume: {resume_text}. Missing skills: {missing_skills}. Similarity score: {similarity_score}."
    response = openai.Completion.create(
        engine=os.getenv("AZURE_OPENAI_ENGINE"),
        prompt=prompt,
        max_tokens=500
    )
    return response.choices[0].text.strip()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to Craft Resume AI"})

@app.route('/parse-job', methods=['POST'])
def parse_job():
    job_description = request.json.get('description', '')
    skills = extract_key_phrases(job_description)
    return jsonify({"skills": skills})

@app.route('/analyze-resume', methods=['POST'])
def analyze_resume_endpoint():
    job_description = request.json.get('job_description', '')
    resume_text = request.json.get('resume_text', '')
    analysis_result = analyze_resume(job_description, resume_text)
    return jsonify({"analysis_result": analysis_result})

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    user_details = request.json.get('user_details', '')
    job_skills = request.json.get('job_skills', '')
    generate_resume_docx(user_details, job_skills)
    return jsonify({"message": "Resume generated successfully"})

@app.route('/upload-resume', methods=['POST'])
def upload_resume():
    file_path = request.json.get('file_path', '')
    container_name = request.json.get('container_name', '')
    upload_to_blob(file_path, container_name)
    return jsonify({"message": "File uploaded successfully"})

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json.get('text', '')
    target_language = request.json.get('target_language', 'en')
    translated_text = translate_text(text, target_language)
    return jsonify({"translated_text": translated_text})

@app.route('/job-insights', methods=['GET'])
def job_insights():
    insights = get_job_insights()
    return jsonify(insights)

if __name__ == '__main__':
    app.run(debug=True)