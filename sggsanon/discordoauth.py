'''
Module that controls Discord Oauth.
'''
from flask import Blueprint,redirect,request
import requests
from app import OAUTH2_CLIENT_ID, OAUTH2_CLIENT_SECRET, REDIRECT_URI, TOKEN_URL, API_URL_BASE


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
    try:
        access_token = response.json()['access_token']
    except KeyError:
        return "<script>alert('Erorr while trying to get userdata, perhaps try again?');document"
    headers = {
        'Authorization': f"Bearer {access_token}",
        'Accept': 'application/json',
    }
    getdata = requests.get(API_URL_BASE, headers=headers)
    return getdata.json()


