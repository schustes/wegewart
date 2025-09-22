# blueprint that checks and manages authentication/authorization before each web request
# Login and logout routes are provided in __init__.py - can it be moved here somehow?
import jwt

from flask import Blueprint
from datetime import datetime
from flask import Flask, render_template, session, jsonify, redirect, url_for,request, redirect
from werkzeug.exceptions import abort
from settings import OAUTH
from authlib.integrations.requests_client import OAuth2Session

from users.domain.services import UserMapper
from users.domain.services.UserDto import UserDto
from users.domain.services.UserService import UserService

from settings import OAUTH

oauthSession = None
userService: UserService = None

def __init__():
    global oauthSession
    oauthSession = createOauth2Session()
    print("OAuth2Session created.")

def set_user_service(user_service):
    global userService
    userService = user_service

def check_auth():    
    if request.path != '/authorize' and request.path != '/logout':
        l = check_session()
        if (l is not None):
            return l

def check_session():
    if not session.get("user_id"):
        print("No user in session, redirecting to login...")
        session['next_url'] = request.url
        return redirect(login())
    elif time_diff_minutes(session.get("token")['expires_at'], datetime.now().timestamp()) < 0:
        print("Authorization token expired, refreshing...")
        refresh_token()
    else:
        print ("token and session are ok")

def login():
    global oauthSession
    oauthSession = createOauth2Session()
    auth_code_uri = oauthSession.create_authorization_url(OAUTH.get("AUTHORIZE_URL"))
    auth_response = auth_code_uri[0]
    session["state"] = auth_code_uri[1]
    return auth_response

def logout():
    print("logging out", session.get("user_id") )
    current_access_token = session.get('access_token')
    session.clear()

    oauthSession.revoke_token(url='https://eu-central-18m8dmenhl.auth.eu-central-1.amazoncognito.com/oauth2/revoke',     
                      token=current_access_token)
    
    logout_url = (
        f"{OAUTH.get("LOGOUT_URL")}"
        f"?client_id={OAUTH.get("CLIENT_ID")}"
        f"&response_type=code"
        f"&scope=openid"
        #f"&logout_uri={OAUTH.get("REDIRECT_URL")}"
        f"&redirect_uri={OAUTH.get("LOGOUT_REDIRECT_URL")}"
    )
    return redirect(logout_url)


def refresh_token():
    refresh_token = session.get('refresh_token')        
    refresh_url = OAUTH.get("TOKEN_URL")
    auth = (oauthSession.client_id , oauthSession.client_secret)

    token = oauthSession.refresh_token(refresh_url, auth=auth, refresh_token=refresh_token)

    session['token'] = token
    session['id_token'] = token.get('id_token')
    session['access_token'] = token.get('access_token')
    session['refresh_token'] = token.get('refresh_token')
    
    print("Token refreshed successfully")   

def authorize_callback(values=None):
    print("authorize callback called")
    authorization_response_from_auth_server = request.url
    state= session.get("state")

    oidc_token = oauthSession.fetch_token(grant_type='authorization_code', state=state, 
                                     authorization_response=authorization_response_from_auth_server)
    
    id_token = oidc_token.get('id_token')
    access_token = oidc_token.get('access_token')        
    refresh_token = oidc_token.get('refresh_token')

    decoded_access_token = decode_jwt(access_token)
    decoded_id_token = decode_jwt(id_token)

    session['token'] = oidc_token
    session['id_token'] = id_token
    session['refresh_token'] = refresh_token
    session['access_token'] = access_token
    session['tenant_id'] = decoded_access_token['membership']
    session['user_id'] = decoded_access_token['sub']

    #check user entry, if not existing, create one   
    user =userService.get_user_by_id(session['user_id'])
    if user is None:
        
        userDto = UserDto(user_id=session['user_id'], 
                                email=decoded_id_token.get('email', ''), 
                                first_name=decoded_id_token.get('first_name', ''), 
                                last_name=decoded_id_token.get('family_name', ''),
                                tenant_id=decoded_access_token['membership'])
        print("Creating new user with id:", session['user_id'], userDto.first_name, '->', decoded_id_token.get('given_name', ''))
        userService.add_user(UserMapper.to_entity(userDto))

    next_url = session.pop('next_url', None)
    if next_url:
      return redirect(next_url)
    return redirect(url_for('index'))


def createOauth2Session():
    return OAuth2Session(
        client_id=OAUTH.get("CLIENT_ID"),
        client_secret=OAUTH.get("CLIENT_SECRET"),
        authorization_endpoint=OAUTH.get("AUTHORIZE_URL"),
        token_endpoint=OAUTH.get("TOKEN_URL"),
        redirect_uri=OAUTH.get("REDIRECT_URL"),
        scope='email openid'        
    )

def decode_jwt( token):
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})
            return decoded_token
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return None
        except jwt.InvalidTokenError:
            print("Invalid token")
            return None  

def time_diff_minutes(ts1, ts2):
    dt1 = datetime.fromtimestamp(ts1)
    dt2 = datetime.fromtimestamp(ts2)
    minutes = (dt1 - dt2).total_seconds() / 60

    diff_seconds = ts1 -ts2
    diff_minutes = diff_seconds / 60 

    return diff_minutes
