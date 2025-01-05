from flask import Flask, request, jsonify, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
import azure_utils

app = Flask(__name__)
app.config.from_object('config')

oauth = OAuth(app)
oauth.register(
    name='azure',
    client_id='your-client-id',
    client_secret='your-client-secret',
    authorize_url='https://login.microsoftonline.com/common/oauth2/v2.0/authorize',
    authorize_params=None,
    access_token_url='https://login.microsoftonline.com/common/oauth2/v2.0/token',
    access_token_params=None,
    refresh_token_url=None,
    redirect_uri='http://localhost:5000/login/authorized',
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/login')
def login():
    redirect_uri = url_for('authorized', _external=True)
    return oauth.azure.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('index'))

@app.route('/login/authorized')
def authorized():
    token = oauth.azure.authorize_access_token()
    if token is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['token'] = token
    return redirect(url_for('index'))

@app.route('/parse-job', methods=['POST'])
def parse_job():
    description = request.json.get('description')
    result = azure_utils.parse_job_description(description)
    return jsonify(result)

@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    job_description = request.json.get('job_description')
    resume_text = request.json.get('resume_text')
    result = azure_utils.analyze_resume(job_description, resume_text)
    return jsonify(result)

@app.route('/generate_resume', methods=['POST'])
def generate_resume():
    user_details = request.json.get('user_details')
    job_skills = request.json.get('job_skills')
    result = azure_utils.generate_resume_docx(user_details, job_skills)
    return jsonify(result)

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file_path = request.json.get('file_path')
    container_name = request.json.get('container_name')
    result = azure_utils.upload_to_blob(file_path, container_name)
    return jsonify(result)

@app.route('/translate', methods=['POST'])
def translate():
    text = request.json.get('text')
    target_language = request.json.get('target_language')
    result = azure_utils.translate_text(text, target_language)
    return jsonify(result)

@app.route('/job_insights', methods=['GET'])
def job_insights():
    result = azure_utils.get_job_insights()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)