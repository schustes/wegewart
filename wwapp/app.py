import sqlite3
from routes.adapters.controllers.ExportWebController import ExportWebController
from routes.adapters.controllers.RouteWebController import RouteWebController
from routes.adapters.gateways.TemplateFileRepository import TemplateFileRepository
from routes.adapters.gateways.TemplateS3Repository import TemplateS3Repository
from routes.domain.services.ExportService import ExportService
from routes.domain.services.RouteService import RouteService
from users.domain.services.UserService import UserService
from users.adapters.gateways.UserDynamoDbRepository import UserDynamoDbRepository
from routes.adapters.gateways.RouteDynamoDbRepository import RouteDynamoDbRepository
from flask import Flask, jsonify, redirect, render_template, url_for
from users.adapters.controllers.UserWebController import UserWebController
from users.domain.entities.UserId import UserId
from authlib.integrations.flask_client import OAuth
import os
from settings import SECRET, SESSION, OAUTH
from frameworks.flask import auth, webapp

#global because of flask blueprint init - needs to injected after app init
users: UserService = None

def index():
    return render_template('index.html')

def setup():
    print("Setting up app...")

    global users
    users = UserService(UserDynamoDbRepository())
    UserWebController(users, webapp)

    routeReader = RouteService(RouteDynamoDbRepository()) #no need for two instances, refactor later
    routeWriter = RouteService(RouteDynamoDbRepository())
    RouteWebController(routeReader, routeWriter, webapp)

    ExportWebController(webapp, export_service=ExportService(TemplateS3Repository(), 
                                                             RouteDynamoDbRepository(),
                                                             users))

setup()

#required for lambda init
with webapp.app_context():
        print("Starting webapp...")
        auth.__init__()
        auth.set_user_service(users)
        webapp.add_url_rule('/index', view_func=index, methods=['GET'])

#the normal way
if __name__ == '__main__':
  with webapp.app_context():
        auth.__init__()
        auth.set_user_service(users)
        webapp.add_url_rule('/index', view_func=index, methods=['GET'])

  webapp.run(debug=False)