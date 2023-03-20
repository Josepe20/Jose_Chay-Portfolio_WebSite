from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, SelectField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

# WTForm
# class CreateProjectForm(FlaskForm):
#     title = StringField("Project Post Title", validators=[DataRequired()])
#     subtitle = StringField("Subtitle", validators=[DataRequired()])
#     author = StringField("Author/ Author's Name", validators=[DataRequired()])
#     img_url = StringField("Project Image URL", validators=[DataRequired(), URL()])
#     body = CKEditorField("Project Description", validators=[DataRequired()])
#     submit = SubmitField("Submit")

class CreateProjectForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField(label='Category',
                           choices=[('Web', 'Web Development'), ('Data', 'Data Science'), ('Auto', 'Automatization'), ('GUIGame', 'GUI/Game'), ('Script', 'Scripting')],
                           validators=[DataRequired()])
    client = StringField("Client", validators=[DataRequired()])
    author = StringField("Authors", validators=[DataRequired()])
    date = StringField("Date, e.g (01 March, 2023)", validators=[DataRequired()])
    project_url = StringField("Project URL", validators=[DataRequired(), URL()])
    img_url_1 = StringField("presentation Image URL_1", validators=[DataRequired(), URL()])
    img_url_2 = StringField("Image URL_2")
    img_url_3 = StringField("Image URL_3")
    description = CKEditorField("Description", validators=[DataRequired()])
    submit = SubmitField("Submit")

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


