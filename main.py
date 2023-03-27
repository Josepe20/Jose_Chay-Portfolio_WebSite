from BaseDatos import app, db
from flask import render_template, redirect, url_for, request, send_from_directory, jsonify
from flask_login import current_user, logout_user


from Forms import UserForm, CreateProjectForm, Delete
from BaseDatos import create_admin, login_admin, admin_only, create_project, Project, edit_project, delete_project, send_email
from BaseDatos import USER_EMAIL, PASSWORD_EMAIL, User
import datetime

## with app.app_context():
##    db.drop_all()
##     db.create_all()

## with app.app_context():
##     db.create_all()

## Routes
@app.route('/')
def home_page():

    with app.app_context():
        all_projects = db.session.query(Project).all()

    return render_template("index.html", is_home=True, current_user=current_user, projects=all_projects)

@app.route('/project-details')
def project_details_page():

    project_id = request.args.get('project_id')
    requested_project = db.session.query(Project).get(project_id)
    return render_template("project-details.html", is_home=False, current_user=current_user, project=requested_project)


# ## Functionalities
@app.route('/get_contact', methods=["POST"])
def get_contact():
    """This function rendering contact page & send information inserted in the contact form"""
    if request.method == "POST":
        try:
            data = request.form

            name_data = data.get('name')
            email_data = data.get('email')
            subject_data = data.get("subject")
            message_data = data.get("message")

            print(f"name: {name_data} "
                  f"email: {email_data} "
                  f"subject: {subject_data} "
                  f"message: {message_data} ")

            print(f'{PASSWORD_EMAIL} '
                  f'{USER_EMAIL}')

            send_email(name=name_data,
                       email=email_data,
                       subject=subject_data,
                       message=message_data)

            return {"response": {"success": "Email has been sent successfully."}}, 200

        except Exception as error:
            return {"response": {"error": "{}".format(error)}}

    else:
        return jsonify(error={"Method Not Allowed": "No post method"}), 405


@app.route('/download')
def download_resume():
    return send_from_directory(directory='static', path="files/CV_JoseChay_Copy.pdf")

@app.route('/secret_register', methods=['GET', 'POST'])
def secret_register():
    user_form = UserForm()
    if user_form.validate_on_submit():
        if db.session.query(User).all() < 1:

            create_admin(name=user_form.Name.data,
                        email=user_form.Email.data,
                        password=user_form.Password.data)

            return redirect(url_for('home_page'))
    return render_template("secret.html", form=user_form, current_user=current_user.is_authenticated)

@app.route('/secret_login', methods=['GET', 'POST'])
def secret_login():
    user_form = UserForm()
    if user_form.validate_on_submit():

        login_admin(name=user_form.Name.data,
                    email=user_form.Email.data,
                    password=user_form.Password.data)

        return redirect(url_for('home_page'))
    return render_template("secret.html", form=user_form, current_user=current_user.is_authenticated)

@app.route('/new_project', methods=['GET', 'POST'])
@admin_only
def create_project_page():
    new_project_form = CreateProjectForm()
    if new_project_form.validate_on_submit():
        create_project(
            title=new_project_form.title.data,
            category=new_project_form.category.data,
            client=new_project_form.client.data,
            author=new_project_form.author.data,
            date=new_project_form.date.data,
            project_url=new_project_form.project_url.data,
            img_url_1=new_project_form.img_url_1.data,
            img_url_2=new_project_form.img_url_2.data,
            img_url_3=new_project_form.img_url_3.data,
            description=new_project_form.description.data
        )
        return redirect(url_for('home_page'))
    return render_template("new_project.html", form=new_project_form, current_user=current_user)

@app.route('/edit', methods=['GET', 'POST'])
@admin_only
def edit_project_page():

    project_id = request.args.get('project_id')
    project_to_edit = db.session.query(Project).get(project_id)

    edit_project_form = CreateProjectForm(
        title=project_to_edit.title,
        category=project_to_edit.category,
        client=project_to_edit.client,
        author=project_to_edit.author,
        date=project_to_edit.date,
        project_url=project_to_edit.project_url,
        img_url_1=project_to_edit.img_url_1,
        img_url_2=project_to_edit.img_url_2,
        img_url_3=project_to_edit.img_url_3,
        description=project_to_edit.description,
    )
    if edit_project_form.validate_on_submit():

        edit_project(project_to_edit=project_to_edit, edit_project_form=edit_project_form)

        return redirect(url_for('home_page'))
    return render_template("edit_project.html", form=edit_project_form, current_user=current_user)

@app.route("/delete_page", methods=['GET', 'POST'])
@admin_only
def delete_page():
    project_id = request.args.get('project_id')
    requested_project = db.session.query(Project).get(project_id)
    delete_form = Delete()
    if delete_form.validate_on_submit():

        delete_project(project_id)

        return redirect(url_for('home_page'))
    return render_template('delete.html', form=delete_form,  current_user=current_user, project=requested_project)


@app.route('/logout')
@admin_only
def logout():
    logout_user()
    return redirect(url_for('home_page'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
