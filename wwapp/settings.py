import os
from pathlib import Path

import boto3
from cachelib import FileSystemCache
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

load_dotenv(dotenv_path=Path(BASE_DIR).resolve().joinpath('env', ENVIRONMENT, '.env'))

SECRET = 'BAD_SECRET_KEY'
SESSION = dict(
    SESSION_PERMANENT=True,
    PERMANENT_SESSION_LIFETIME=480,
    SESSION_TYPE="dynamodb",
    SESSION_DYNAMODB=boto3.resource('dynamodb', region_name='eu-central-1', endpoint_url=os.getenv('DYNAMODB_ENDPOINT_URL')),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_DOMAIN=False,
    SERVER_NAME='localhost:5000'
)

OAUTH = dict(
    CLIENT_ID=os.getenv('CLIENT_ID'),
    CLIENT_SECRET=os.getenv('CLIENT_SECRET'),
    TOKEN_URL=os.getenv('TOKEN_URL'),
    AUTHORIZE_URL=os.getenv('AUTHORIZE_URL'),
    USER_URL=os.getenv('USER_URL'),
    REDIRECT_URL=os.getenv('REDIRECT_URL'),
    LOGOUT_URL=os.getenv('LOGOUT_URL'),
    LOGOUT_REDIRECT_URL=os.getenv('LOGOUT_REDIRECT_URL')
    
)
DYNAMODB = dict(
    REGION='eu-central-1',
    ENDPOINT_URL=os.getenv('DYNAMODB_ENDPOINT_URL'),
)