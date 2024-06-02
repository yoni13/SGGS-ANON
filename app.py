 # Global APP settings
from flask import Flask, request
from flask_mail import Mail
from pymongo import MongoClient
import os
from flask_limiter import Limiter
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ['app_secret_key']
app.config['CSRF_SECRET_KEY'] = os.urandom(24)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
csrf = CSRFProtect(app)

def get_remote_address():
    return request.headers.get('cf-connecting-ip') if request.headers.get('cf-connecting-ip') else request.remote_addr


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)


client = MongoClient(os.environ['DATABASE_URL'])
db = client["message"]



app.config.update(
    DEBUG=False,
    MAIL_SERVER='smtp-relay.brevo.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_DEFAULT_SENDER=('admin', 'admin@nicewhite.eu.org'),
    MAIL_MAX_EMAILS=10,
    MAIL_USERNAME='6c6343001@smtp-brevo.com',
    MAIL_PASSWORD=os.environ['email_key']
)
mail = Mail(app)



def get_mail():
    return mail

from sggsanon import api, moderation, static_files, frontend, opengraph
app.register_blueprint(api.api)
app.register_blueprint(moderation.mod)
app.register_blueprint(static_files.static_files)
app.register_blueprint(frontend.frontend)
app.register_blueprint(opengraph.opengraph)


if __name__ == "__main__":
    app.run(port=8080, debug=True, host='0.0.0.0')
