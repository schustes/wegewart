from flask import Flask, render_template
from werkzeug.exceptions import abort
from users.usecases.ForReadingUsers import ForReadingUsers

class UserWebController():

    def __init__(self, users: ForReadingUsers, webapp: Flask):
        self.users = users
        self.webapp = webapp
        #self.webapp.route('/index') (self.get_all_users)
        #self.webapp.route('/') (self.get_all_users)
        self.webapp.add_url_rule('/index', view_func=self.get_all_users, methods=['GET'])
        self.webapp.add_url_rule('/', view_func=self.get_all_users, methods=['GET'])
        self.webapp.add_url_rule('/<user_id>', view_func=self.get_user_by_id, methods=['GET'])

    def get_all_users(self):
        users = self.users.get_all_users()
        return render_template('index.html', users=users)

    def get_user_by_id(self, user_id):
        print(f"get_user_by_id: {user_id}")
        user = self.users.get_user_by_id(user_id)
        if user is None:
            abort(404)
        #userEntity = user.rootEntity if user else None
        #print(user.userEntity.user_id)

        return render_template('user.html', user=user)

