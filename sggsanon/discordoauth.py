'''
Module that controls Discord Oauth.
'''
from flask import Blueprint,redirect,request
import requests
from app import OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, REDIRECT_URI, AUTHORIZE_URL, TOKEN_URL, API_URL_BASE


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

    return response_data['access_token']

 

@discordoauth.route('/auth/discord/login')
def discordoauthlogin():
    params = {
        'client_id': OAUTH2_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': 'identify guilds',
    }
    url = f"{AUTHORIZE_URL}?{requests.compat.urlencode(params)}"
    return redirect(url)