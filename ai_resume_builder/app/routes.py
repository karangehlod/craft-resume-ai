from flask import Blueprint, render_template, request, redirect, url_for

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