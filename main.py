from BaseDatos import app, db
from flask import render_template, redirect, url_for, request, send_from_directory
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

from Forms import UserForm
from BaseDatos import create_admin, login_admin
import datetime

# with app.app_context():
#     db.drop_all()
#     db.create_all()

## Routes
@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/project-details')
def project_details_page():
    return render_template("project-details.html")


## Functionalities
@app.route('/download')
def download_resume():
    return send_from_directory(directory='static', path="files/CV_Jose_Chay _Copy.pdf")

@app.route('/secret', methods=['GET', 'POST'])
def secret_page():
    user_form = UserForm()
    if user_form.validate_on_submit():

        #### I won't use create user function anymore, but I will let it here :D
        ## create_admin(name=user_form.Name.data,
        ##             email=user_form.Email.data,
        ##             password=user_form.Password.data)

        login_admin(name=user_form.Name.data,
                    email=user_form.Email.data,
                    password=user_form.Password.data)

        return redirect(url_for('home_page', logged_in=True))
    return render_template("secret.html", form=user_form, logged_in=current_user.is_authenticated)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page', logged_in=False))

if __name__ == "__main__":
    app.run(debug=True)
