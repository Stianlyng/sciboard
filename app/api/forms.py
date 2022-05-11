from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField,FileField
from wtforms.validators import  DataRequired, length
from flask_wtf.file import FileField, FileRequired



class UploadDocumentForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')