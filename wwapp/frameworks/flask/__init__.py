import os
from flask import Blueprint
from datetime import datetime
from flask import Flask, render_template, session, jsonify, redirect, url_for,request, redirect
from flask_session import Session
from werkzeug.exceptions import abort
from frameworks.flask import auth
from settings import SESSION
from users.usecases.ForReadingUsers import ForReadingUsers
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session

# Create Flask web application instance and specific dependcies to flask_oauth inside frameworks circle.
# Flask Webapp is referenced in the global app.py after init and setup.
# Defines login/logoute routes -> can it be moved auth.py?
webapp = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

webapp.secret_key = os.urandom(24) 

print("webapp instance created")

webapp.config.update(SESSION)
session = Session()
session.init_app(webapp)

bp = Blueprint('app', __name__)
bp.before_app_request(auth.check_auth)

print("auth aspect injected as flask blueprint")

webapp.route('/authorize') (auth.authorize_callback)
webapp.route('/logout') (auth.logout)

webapp.register_blueprint(bp)
