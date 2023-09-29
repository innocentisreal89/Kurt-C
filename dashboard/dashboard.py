from flask import Blueprint,request,redirect, make_response, render_template, flash, url_for
from flask_login import  login_required, current_user
from db import db
from model.url import Url, is_valid_url
from extension import cache, limiter





blp =  Blueprint('dashboard',  __name__, template_folder='templates' )

@blp.route('/dashboard', methods=['GET','POST'])
# @cache.cached(timeout=3600)
@limiter.limit("10/minute") 
@login_required
def index():
    '''getting the urls of a specific user'''
    urls = Url.query.filter_by(user_id=current_user.id).all()

    if not urls:
        flash('Oops! No Url history found')
    return render_template('index.html',urls=urls)



# @app.route('/')
# def home():
#     todo_list = Todo.query.all()
#     return render_template('index.html', todo_list=todo_list)
