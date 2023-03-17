from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

# WTForm
class CreateProjectForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

#
# # WTForm Sing UP
# class UserForm(FlaskForm):
#     Name = StringField("Name", validators=[DataRequired()])
#     Email = EmailField("Email", validators=[DataRequired(), Email()])
#     Password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField("Sing Up")

# WTForm
class UserForm(FlaskForm):
    Name = StringField("Name", validators=[DataRequired()])
    Email = EmailField("Email", validators=[DataRequired(), Email()])
    Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField("Log In")


