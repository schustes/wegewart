from flask import Flask, render_template, session, jsonify, redirect, url_for,request, redirect
from werkzeug.exceptions import abort
from users.adapters.controllers import UserDictMapper
from users.usecases.ForReadingUsers import ForReadingUsers
from authlib.integrations.flask_client import OAuth
from authlib.integrations.requests_client import OAuth2Session

class UserWebController():

    def __init__(self, users: ForReadingUsers, webapp: Flask):
        self.users = users
        self.webapp = webapp
        self.webapp.add_url_rule('/app/users', view_func=self.get_all_users, methods=['GET'])
        self.webapp.add_url_rule('/app/users/<user_id>', view_func=self.get_user_by_id, methods=['GET'])

    def get_all_users(self):
        users = [UserDictMapper.from_user_dto_to_dict(user) for user in self.users.get_all_users()]
        return render_template('users.html', users=users, tenant_id=session.get('tenant_id'))

    def get_user_by_id(self, user_id):
        user = self.users.get_user_by_id(user_id)
        if user is None:
            abort(404)
        return render_template('user.html', user=UserDictMapper.from_user_dto_to_dict(user), tenant_id=session.get('tenant_id'))
    