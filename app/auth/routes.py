from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm,ResetPasswordRequestForm,ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email,send_vertification_link_email

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.frontpage'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        #next_page = request.args.get('next')
        return redirect(url_for('main.frontpage'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.frontpage'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.frontpage'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data,first_name=form.first.data,last_name=form.last.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.registerSuccess', user_id=user.id))
    return render_template('auth/register.html', title='Register',
                           form=form)

@bp.route('/registration-successful', methods=['GET', 'POST'])
def registerSuccess():
    if current_user.is_authenticated:
        return redirect(url_for('main.frontpage'))
    # Get the userid returned by the redirect after registration success in auth.register
    user_id_from_ref = request.args.get('user_id')

    user = User.query.get(user_id_from_ref)
    # Send mail
    send_vertification_link_email(user)
    return render_template('auth/vertification-notice.html',firstname=user.first_name)


@bp.route('/activate-account/<token>', methods=['GET', 'POST'])
def activateAccount(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.frontpage'))
    #user = User.verify_reset_password_token(token)

    hardkodetToken = "yoloswag"

    if token == hardkodetToken:
        user = User.query.get(12)
        user.vertified = True
        db.session.commit()
        return render_template('auth/vertification-success.html')
    else:
        return redirect(url_for('api.not_found_error'))

@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.frontpage'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            'Check your email for the instructions to reset your password')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.frontpage'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.frontpage'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
