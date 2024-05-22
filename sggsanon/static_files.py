from flask import Blueprint, render_template,redirect,request


static_files = Blueprint('static_files', __name__)

@static_files.route('/policy')
def tos():
    return render_template('policy.html')

@static_files.route('/favicon.ico')
def favicon():
    return redirect('/static/img/logo.png')

@static_files.route('/robots.txt')
def robots():
    if request.host == 'sggs-indev-sggsanon.nicewhite.xyz':
        return redirect('/static/robots_dev.txt')
    if request.host == 'sggsanon.nicewhite.xyz':
        return redirect('/static/robots_prod.txt')