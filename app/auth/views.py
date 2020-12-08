from . import auth
from flask import render_template,redirect,url_for,flash,request
from ..models import User,Subscriber
from .forms import RegistrationForm,LoginForm,SubscriptionForm
from .. import db
from flask_login import login_user,logout_user,login_required
from ..email import mail_message


@auth.route('/login',methods = ["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        
        if user is not None and user.passwd == login_form.password.data:
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.blogs'))

        flash('Invalid username or Password')
    return render_template('auth/login.html',login_form = login_form)

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,passwd = form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to Zuri's women's blog","email/welcome_user",user.email,user=user)
        return redirect(url_for('main.login'))
    return render_template('auth/register.html',registration_form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route('/subscriber', methods=['GET','POST'])
def subscriber():
    subscriber_form=SubscriptionForm()
    if subscriber_form.validate_on_submit():
        email = subscriber_form.email.data
        subscriber = Subscriber(email = email)

        db.session.add(subscriber)
        db.session.commit()
        flash('Thank you for subscribing you will receive an email shortly')
    return render_template('auth/subscriber.html',subscriber= subscriber_form.email.data,subscriber_form=subscriber_form)   