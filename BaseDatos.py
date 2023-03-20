from flask import Flask, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
ckeditor = CKEditor(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

#Create admin-only decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #If id is not 1 then return abort with 403 error
        if current_user.id != 1:
            return abort(403)
        #Otherwise continue with the route function
        return f(*args, **kwargs)
    return decorated_function

# CONFIGURE TABLE
# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(1000), unique=True, nullable=False)

# CONFIGURE TABLE
# CREATE TABLE IN DB
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    category = db.Column(db.String(250), nullable=False)
    client = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    project_url = db.Column(db.String(1000), nullable=False)
    img_url_1 = db.Column(db.String(1000), nullable=False)
    img_url_2 = db.Column(db.String(1000), nullable=True)
    img_url_3 = db.Column(db.String(1000), nullable=True)
    description = db.Column(db.Text, nullable=False)


def create_admin(name, email, password):
    # hash and salt password
    hash_and_salted_password = generate_password_hash(
        password=password,
        method="pbkdf2:sha256",
        salt_length=8,
    )

    new_user = User(
        email=email,
        password=hash_and_salted_password,
        name=name,
    )

    db.session.add(new_user)
    db.session.commit()


def login_admin(name, email, password):

    # Find user by email entered.
    user = db.session.query(User).first()

    if name == user.name:
        if email == user.email:
            # Check stored password hash against entered password hashed.
            if check_password_hash(user.password, password):
                login_user(user)

def create_project(title, category, client, author, date, project_url,
                   img_url_1, img_url_2, img_url_3, description,):

    new_project = Project(
        title=title,
        category=category,
        client=client,
        author=author,
        date=date,
        project_url=project_url,
        img_url_1=img_url_1,
        img_url_2=img_url_2,
        img_url_3=img_url_3,
        description=description
    )

    db.session.add(new_project)
    db.session.commit()

def edit_project(project_to_edit, edit_project_form):

    project_to_edit.title = edit_project_form.title.data,
    project_to_edit.category = edit_project_form.category.data,
    project_to_edit.client = edit_project_form.client.data,
    project_to_edit.author = edit_project_form.author.data,
    project_to_edit.date = edit_project_form.date.data,
    project_to_edit.project_url = edit_project_form.project_url.data,
    project_to_edit.img_url_1 = edit_project_form.img_url_1.data,
    project_to_edit.img_url_2 = edit_project_form.img_url_2.data,
    project_to_edit.img_url_3 = edit_project_form.img_url_3.data,
    project_to_edit.description = edit_project_form.description.data

    db.session.commit()


