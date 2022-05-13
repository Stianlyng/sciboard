from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask_wtf.file import FileField, FileRequired



class UploadDocumentForm(FlaskForm):
    file = FileField(validators=[FileRequired()])
    submit = SubmitField('Submit')