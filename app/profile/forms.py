from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import ValidationError, optional,length
from app.models import User



class UploadThumbnailForm(FlaskForm):

    image = FileField()
    username = StringField('Username')
    first = StringField('Firstname')
    last = StringField('Lastname')
    about = TextAreaField([optional(), length(max=10000)])
    submit = SubmitField('Change')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')



