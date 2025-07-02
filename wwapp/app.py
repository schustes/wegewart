import sqlite3
from users.domain.usecases.UserRepository import UserRepository
from users.domain.services.UserService import UserService
from users.adapters.gateways.UserInMemoryRepository import UserInMemoryRepository
from users.adapters.gateways.UserDynamoDbRepository import UserDynamoDbRepository
from flask import Flask, jsonify
from users.adapters.controllers.UserWebController import UserWebController
from users.domain.entities.UserId import UserId

webapp = Flask(__name__,
            static_url_path='', 
            static_folder='frameworks/flask-ui/static',
            template_folder='frameworks/flask-ui/templates')


con: sqlite3.Connection = None
userRepository: UserRepository = None
userWebController = None
users = None

def get_db_connection():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    return con

def setup():
    global con 
    #con = get_db_connection()
    global userRepository
    #userRepository = UserInMemoryRepository(con)
    userRepository = UserDynamoDbRepository()
    global userWebController
    users = UserService(userRepository)
    userWebController = UserWebController(users, webapp)

setup()

if __name__ == '__main__':
    #get_db_connection()
    #setup()
    webapp.run(debug=True)