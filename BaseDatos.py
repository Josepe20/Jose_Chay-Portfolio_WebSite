from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(int(user_id))

# CONFIGURE TABLE
# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(1000), unique=True, nullable=False)

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

