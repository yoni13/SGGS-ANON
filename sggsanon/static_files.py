from flask import Blueprint, render_template,redirect


static_files = Blueprint('static_files', __name__)

@static_files.route('/policy')
def tos():
    return render_template('policy.html')

@static_files.route('/favicon.ico')
def favicon():
    return redirect('/static/img/logo.png')