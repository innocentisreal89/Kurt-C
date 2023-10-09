from flask import Blueprint,request,redirect, make_response, render_template, flash, url_for
from flask_login import  login_required, current_user
from db import db
from model.url import Url, is_valid_url
from extension import cache, limiter




blp =  Blueprint('url',  __name__, template_folder='templates/url', static_folder='static', static_url_path='urls')



# @blp.route('/')
# def home():
#     urls = Url.query.order_by(Url.created).all()
#     return render_template('index.html', user=current_user, urls=urls)

    
@blp.route('/url_shortener', methods=['GET', 'POST'])
@login_required
def shorten_url():
         
    if request.method == 'POST':
        org_url = request.form.get('original_url')
        short_id = request.form.get('custom_id') or None
        error = None

        # #   Validating the Url
        if not is_valid_url(org_url):
                flash('Invalid Url', message='error')
                     

        #   checking if url exist in the user's db (reason for the 'user_id=current_user' )
        url = Url.query.filter_by(org_url=org_url, user_id=current_user.id).first()
        if  url:
            flash('This Url already exist')
            return redirect(url_for('url.shorten_url'))
        elif url and url.short_id == short_id:
            flash('This Url and custom id already exist', message='error')
            return redirect(url_for('url.shorten_url'))

        #bcos of reuasbility of short id, i will comment this
        # url = Url.query.filter_by(short_id=short_id, user_id=current_user).first()
        # if url :
        #         flash(f'{short_id} already exist!', message='warning')
        #         return redirect(url_for('shorten_url'))


        new_link = Url(
            org_url = org_url,
            short_id = short_id,
            user_id = current_user.id
        )
        #   logic for customizing short url
        if short_id:
            new_link.short_id = short_id
            new_link.qr_code = new_link.generateqr()
         
        new_link.save()
        flash('Url shortened successfully')
        return redirect(url_for('dashboard.index'))
    
    return render_template('create.html')

        # return render_template('success.html', user_id=current_user.id, new_link=new_link)# redirect to a function that  will show them what theyve created
        


    
"""Redirect to the original url"""    
@blp.route("/<string:short_id>/redirect")
@login_required
@cache.cached(timeout=3600)
@limiter.limit("10/minute")  # Allow 10 requests per minute
def redirect_url(short_id):
    new_link = Url.query.filter_by(short_id=short_id).first()
    if new_link:
        new_link.clicks += 1
        db.session.commit()
        return redirect(new_link.org_url)# taking the user out of the site
    else:
        # abort(404, message="Url not found")
        flash('Url not found')
    return render_template('index.html')



"""Get the QR code for a short url"""
@blp.route("/<string:short_id>/qr_code")
@cache.cached(timeout=3600) # Cache for 1 hour (3600 seconds)
@limiter.limit("10/minute")  # Allow 10 requests per minute
def qr_code(short_id):
    link = Url.query.filter_by(short_id=short_id).first_or_404()
    response = make_response(link.qr_code)
    response.headers.set("Content-Type", "image/jpeg")
    return response




@blp.route('/link_history')
@cache.cached(timeout=3600)
def link_history():
    '''getting the urls of a specific user'''
    urls = Url.query.filter_by(user_id=current_user).all()

    if not urls:
        flash('Oops! No Url history found')
    return urls


# @blp.route('/<string:short_id>/edit' , methods=['GET', 'POST'])
# @login_required
# def update(short_id):
#     link = Url.query.filter_by(short_id=short_id).first()
#     if link:
#         if request.method == 'POST':
#             link.short_id = request.form.get('short_id')
#             link.short_id = link.short_id
#             link.qr_code = link.generateqr()
#             db.session.commit()
#             return redirect(url_for('dashboard.index'))
    
#     return render_template('edit.html', url=link)


@blp.route('/<string:short_id>/delete' )
@login_required
def delete(short_id):
    link = Url.query.filter_by(short_id=short_id).first()
    if link:
        link.delete()
        return redirect(url_for('dashboard.index'))
    
    # return render_template('edit.html', url=link)

