from db import db
from flask_login import UserMixin, current_user
from functools import wraps
from flask_smorest import abort
from datetime import datetime
import operator, random


def code_gen(prefix):
    code = random.randint(1000,90000)
    code = str(code)
    return prefix + code


class Admin(db.Model,UserMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
       

    def __repr__(self):
        return f'<User {self.username}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    
def admin_required(function):
    @wraps(function)
    def wrapper(*args, **kwarg):
        loggedUser = current_user #getting the logged in user identity
        #checking if the user is an admin
        if not loggedUser.endswith('io.ict.ng'):
            abort(401, message="Restricted Access")
        return function(*args, **kwarg)
    return wrapper

# print(check_last_email_char(email))
def check_last_email_char(str):
    n = 9
    str2 = operator.getitem(str, slice(len(str)-n, len(str)))
    return str2



