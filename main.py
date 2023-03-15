from flask import Flask
from flask_bootstrap import Bootstrap
from flask import render_template, redirect, url_for, request, send_from_directory
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

## Routes
@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/resume')
def resume_page():
    return render_template("resume.html")

@app.route('/portfolio')
def portfolio_page():
    return render_template("portfolio.html")

@app.route('/services')
def services_page():
    return render_template("services.html")

@app.route('/inner')
def inner_page():
    return render_template("inner-page.html")

@app.route('/portfolio-details')
def portfolio_details_page():
    return render_template("portfolio-details.html")

## Functionalities
@app.route('/download')
def download_resume():
    return send_from_directory(directory='static', path="files/CV_Jose_Chay _Copy.pdf")

if __name__ == "__main__":
    app.run(debug=True)
