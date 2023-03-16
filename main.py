from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, url_for, request, send_from_directory
from Forms import UserForm
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

## Routes
@app.route('/')
def home_page():
    return render_template("index.html", is_home=True)

@app.route('/project-details')
def project_details_page():
    return render_template("project-details.html")

@app.route('/secret', methods=['GET', 'POST'])
def secret_page():
    user_form = UserForm()
    if user_form.validate_on_submit():
        name = user_form.Name.data
        email = user_form.Email.data
        password = user_form.Password.data

    return render_template("secret.html", form=user_form)

## Functionalities
@app.route('/download')
def download_resume():
    return send_from_directory(directory='static', path="files/CV_Jose_Chay _Copy.pdf")

if __name__ == "__main__":
    app.run(debug=True)
