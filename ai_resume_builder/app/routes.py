from flask import Blueprint, render_template, request, redirect, url_for, jsonify
import logging
from azure_utils import extract_key_phrases_in_batches, identify_missing_skills

bp = Blueprint('main', __name__)

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle form submission
        return redirect(url_for('main.result'))
    return render_template('index.html')

@bp.route('/result')
def result():
    # Display the generated resume
    return render_template('result.html')

@bp.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    job_description = request.form.get('job_description')
    resume_text = request.form.get('resume_text')
    resume_file = request.files.get('resume_file')

    logging.info(f"Received job description: {job_description}")
    logging.info(f"Received resume text: {resume_text}")
    logging.info(f"Received resume file: {resume_file}")

    if resume_file:
        try:
            resume_text = resume_file.read().decode('utf-8', errors='ignore')
        except UnicodeDecodeError:
            logging.error("Failed to decode resume file")
            return jsonify({"error": "Failed to decode resume file"}), 400

    job_skills = extract_key_phrases_in_batches(job_description)
    try:
        resume_skills = extract_key_phrases_in_batches(resume_text)
    except AttributeError as e:
        if "DocumentError" in str(e):
            logging.error("Document too large to be processed")
            return jsonify({"error": "Document too large to be processed. Please limit document size to 5120 text elements."}), 400
        else:
            raise

    missing_skills = identify_missing_skills(job_skills, resume_skills)
    score = (len(resume_skills) - len(missing_skills)) / len(job_skills) * 100
    suggested_keywords = [skill for skill in job_skills if skill not in resume_skills]

    logging.info(f"Missing skills: {missing_skills}")
    logging.info(f"Score: {score}")
    logging.info(f"Suggested keywords: {suggested_keywords}")

    return jsonify({"missing_skills": missing_skills, "score": score, "suggested_keywords": suggested_keywords})