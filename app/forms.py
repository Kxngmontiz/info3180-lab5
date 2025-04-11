# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, DataRequired

from flask_wtf.file import FileAllowed, FileRequired, FileField

# Add any form classes for Flask-WTF here

class MovieForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    poster = FileField("Poster Upload", validators=[FileRequired(), FileAllowed(["jpg", "jpeg", "png"], "Images Only")])