'''
Module that controls Discord Oauth.
'''
from flask import Blueprint, render_template,redirect,request



discordoauth = Blueprint('discordoauth', __name__)

@discordoauth.route('/auth/discord/callback')
def discord_callback():
    code = request.args.get('code')
    data = {
        'client_id': OAUTH2_CLIENT_ID,
        'client_secret': OAUTH2_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(TOKEN_URL, data=data, headers=headers)
    response_data = response.json()

    session['access_token'] = response_data['access_token']
    return redirect(url_for('index'))