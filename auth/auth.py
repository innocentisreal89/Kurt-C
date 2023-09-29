from flask import Blueprint,request,redirect, make_response, render_template, flash, url_for
from passlib.hash import pbkdf2_sha256
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import   login_user, logout_user, login_required
from model.user import User
from datetime import timedelta
from extension import cache, limiter


blp =  Blueprint('auth',  __name__, template_folder='templates/auth')



@blp.route('/register', methods= ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password= request.form.get('confirm_password')

        # error =None
        if username  == "" or email=='':
            # error = 'Username is required.'
            flash( 'Username and email are required.')
            return redirect(url_for('auth.register'))
        elif password=="":
            # error = 'Password is required.'
            flash( 'Password is required.', 'error')
            return redirect(url_for('auth.register'))
        elif password != confirm_password:
            # error = 'incorrect password'
            flash('incorrect password','error')
            return redirect(url_for('auth.register'))
        
        user = User.query.filter_by(email=email.lower()).first()
       
        if user:
            # error=f'User with {user} already exist!'
            flash( f'User with this email already exist!', 'error')
            return redirect(url_for('auth.register'))
        elif User.query.filter_by(username=username.lower()).first():
            flash( f'User with username already exist!', 'error')
            return redirect(url_for('auth.register'))
        
        
        user = User(
            username = username.lower(),
            email = email.lower(),
            password = generate_password_hash(password)
        )

        user.save()
        flash('Registration successful, redirecting now', 'success')
        # login_user(user, remember=True)
        # return redirect(url_for('dashboard.index'))
        return redirect(url_for('auth.login'))
    # flash(error)
    return render_template('register.html')  

@blp.route('/login', methods=['GET','POST'])
# @cache.cached(timeout=30)
@limiter.limit("10 per minute")
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email.lower()).first()
        # if user and check_password_hash(user.password,password):
        #     login_user(user, remember=True)
        #     flash("Logged in sucessfully")
        #     return redirect(url_for('dashboard.index'))
            
        # flash('Invalid Credentials!')
        if user:
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash('You are now logged in.')
                return redirect(url_for('dashboard.index'))
            
            if (user and check_password_hash(user.password, password)) == False:
                flash('Please provide valid credentials.')
                return redirect(url_for('auth.login'))

        else:
            flash('Account not found. Please sign up to continue.')
            return redirect(url_for('auth.register'))
    return render_template('login.html')



@blp.route("/logout")
@login_required
def logout(): 
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
       