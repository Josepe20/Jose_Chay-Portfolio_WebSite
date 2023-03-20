from BaseDatos import app, db
from flask import render_template, redirect, url_for, request, send_from_directory
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


from Forms import UserForm, CreateProjectForm
from BaseDatos import create_admin, login_admin, admin_only, create_project, Project, edit_project
import datetime

# with app.app_context():
#     db.drop_all()
#     db.create_all()

# with app.app_context():
#     db.create_all()

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


## Functionalities
@app.route('/download')
def download_resume():
    return send_from_directory(directory='static', path="files/CV_Jose_Chay_Copy.pdf")

@app.route('/secret', methods=['GET', 'POST'])
def secret_page():
    user_form = UserForm()
    if user_form.validate_on_submit():

        #### I won't use create user function anymore, but I will let it here :D
        # create_admin(name=user_form.Name.data,
        #             email=user_form.Email.data,
        #             password=user_form.Password.data)

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
        description=project_to_edit.description
    )
    if edit_project_form.validate_on_submit():

        edit_project(project_to_edit=project_to_edit,
                     edit_project_form=edit_project_form)

        return redirect(url_for('home_page'))
    return render_template("edit_project.html", form=edit_project_form, current_user=current_user)

@app.route("/delete_page")
@admin_only
def delete_page():
    project_id = request.args.get('project_id')
    return redirect(url_for('home_page'))

@app.route("/delete")
@admin_only
def delete():
    project_id = request.args.get('project_id')
    project_to_delete = db.session.query(Project).get(project_id)
    db.session.delete(project_to_delete)
    db.session.commit()
    return redirect(url_for('home_page'))

@app.route('/logout')
@admin_only
def logout():
    logout_user()
    return redirect(url_for('home_page'))

if __name__ == "__main__":
    app.run(debug=True)
