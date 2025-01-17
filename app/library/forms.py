from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,DateField, SelectField,SubmitField
from wtforms.validators import DataRequired, optional,length


class MetadataForm(FlaskForm):
    title = StringField(validators=[DataRequired()])
    authors = StringField(validators=[DataRequired()])
    description = TextAreaField([optional(), length(max=10000)])
    date = DateField(format='%Y-%m-%d')
    access = SelectField(choices=[],coerce=int,validators=[DataRequired()])
    type = SelectField(choices=[],coerce=int,validators=[DataRequired()])
    catalog = SelectField(choices=[],coerce=int,validators=[DataRequired()], render_kw={'hx-get': '/library/getCatalogHasTagCategory','hx-target': '#categories-selector'})
    tags = StringField(validators=[DataRequired()])
    submit = SubmitField('Submit')


class CommentForm(FlaskForm):
    comment = TextAreaField( length(max=350), validators=[DataRequired()])
    submit = SubmitField('post')
