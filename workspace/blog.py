from flask import Blueprint, flash, render_template, g, redirect, url_for, request, session
from werkzeug.exceptions import abort
from .auth import login_required
from workspace.db import get_db


bp = Blueprint("blog", __name__)


@bp.route("/profile", methods=("GET", "POST"))
def profile():
    # Define default values for the variables
    email = 'No Email Provided'
    username = 'No Username Provided'
    name = 'No Name Provided'
    surname = 'No Surname Provided'
    dob = 'No Date of Birth Provided'
    sex = 'No Sex Provided'
    
    if request.method == "POST":
        email = request.form.get("email", 'No Email Provided')
        username = request.form.get("username", 'No Username Provided')
        name = request.form.get("name", 'No Name Provided')
        surname = request.form.get("surname", 'No Surname Provided')
        dob = request.form.get("dob", 'No Date of Birth Provided')
        sex = request.form.get("sex", 'No Sex Provided')
        
        # Save form data to session
        session['email'] = email
        session['username'] = username
        session['name'] = name
        session['surname'] = surname
        session['dob'] = dob
        session['sex'] = sex
        
        db = get_db()
        error = None
        
        if error is None:
            try:
                db.execute(
                    "INSERT INTO diagnosis (email, username, name, surname, dob, sex) VALUES (?, ?, ?, ?, ?, ?)",
                    (email, username, name, surname, dob, sex),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            else:
                
                return redirect(url_for("blog.home"))

        flash(error)
    
    # Retrieve user data from session if it exists, otherwise use defaults   
    email = session.get('email', 'No Email Provided')
    username = session.get('username', 'No Username Provided')
    name = session.get('name', 'No Name Provided')
    surname = session.get('surname', 'No Surname Provided')
    dob = session.get('dob', 'No Date of Birth Provided')
    sex = session.get('sex', 'No Sex Provided')
    
    return render_template("main/profile.html", email=email, username=username, name=name, surname=surname, dob=dob, sex=sex)


@bp.route("/home")
@login_required
def home():
    return render_template("main/home.html")

@bp.route("/medical-qr-alert")
@login_required
def medical_qr_alert():
    return render_template("main/alert.html")

@bp.route('/diagnosis')
@login_required
def diagnosis():
    return render_template("main/check.html")

@bp.route('/appointment', methods=["GET", "POST"])
@login_required
def appointment():
    return render_template("main/checkUp.html")