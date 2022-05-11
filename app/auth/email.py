from flask import render_template, current_app
from app.email import send_email




def send_vertification_link_email(user,token):
    send_email('[Sciboard] Activate your account!',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/vertification_link.txt',
                                         user=user, token=token),
               html_body=render_template('email/vertification_link.html',
                                         user=user, token=token))








def send_password_reset_email(user,token):
    send_email('[Sciboard] Reset Your Password',
               sender=current_app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
