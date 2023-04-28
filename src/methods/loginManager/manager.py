from flask_login import logout_user, login_user, login_required, LoginManager, UserMixin
from flask import request, render_template, redirect, flash
from flask import redirect
from flask.views import MethodView

class User(UserMixin):
    def __init__(self, usrcod, usrnome, usrsen, active=True):
        self.usrcod = usrcod
        self.usrnome = usrnome
        self.usrsen = usrsen

    @property
    def is_authenticated(self):
        return True  

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.usrcod)
    