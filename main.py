import os
import sqlite3
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from functools import wraps
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from functions import login_required, create_table, apology_exists, apology_match, apology_login, apology_login2

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

current = os.path.dirname(os.path.abspath(__file__))

m_id=""
m_id2=""


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        # Redirect user to home page
        return redirect("/add_profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()
        read = "SELECT * FROM profile WHERE username = ?"
        db.execute(read, [session["user_id"]])
        profiles = db.fetchall()

        print(profiles)

        pr = ["", "", "", ""]

        for i in range(len(profiles)):

            if profiles[i] is None:
                pr[i] = ""

            else:
                pr[i] = "true"

        return render_template("index.html", p=pr)


@app.route("/main", methods=["GET"])
def main():
    if request.method == "GET":
        session.clear()
        create_table()
        return render_template("main.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    create_table()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()
        read = "SELECT * FROM users WHERE username = ?"
        db.execute(read, [username])
        user_one = db.fetchone()
        print(user_one)
        print(password)
        # Ensure username exists and password is correct
        if user_one is None:
            return apology_login()

        if user_one[1] != password:
            return apology_login2()

        # Remember which user has logged in
        session["user_id"] = user_one[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()

        read = "SELECT * FROM users WHERE username = ?"
        db.execute(read, [username])
        rows = db.fetchone()
        print(rows)

        # Ensure the username doesn't exists
        if rows is not None:
            return apology_exists()

        # Ensure passwords match
        elif not password == password2:
            return apology_match()

        else:

            # Insert the new user

            insert = "INSERT INTO users (username, password) VALUES (?, ?) "
            db.execute(insert, (username, password,))
            connection.commit()
            # Redirect user to home page
            return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("signup.html")


@app.route("/add_profile", methods=["GET", "POST"])
@login_required
def add_profile():

    if request.method == "POST":

        profile_name = request.form.get("profile_name")

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()

        insert = "INSERT INTO profile (p_name, username) VALUES (?, ?) "
        db.execute(insert, (profile_name, session["user_id"],))
        connection.commit()

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("add_profile.html")


@app.route("/home", methods=["GET", "POST"])
@login_required
def home():

    if request.method == "POST":

        global m_id
        global m_id2
        m_id = request.form.get("moviebutton")
        m_id2 = request.form.get("moviebutton2")
        print("check")
        print(m_id)
        print(m_id2)

        # Redirect user to home page
        return redirect("/movie")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()
        read = "SELECT * FROM movies WHERE type = 'popular'"
        db.execute(read)
        movies = db.fetchall()

        print(movies)

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()
        read = "SELECT * FROM movies WHERE type = 'bolly'"
        db.execute(read)
        moviesb = db.fetchall()

        return render_template("home.html", movies=movies, moviesb=moviesb)


@app.route("/movie", methods=["GET", "POST"])
@login_required
def movie():

    global m_id
    global m_id2

    if m_id is None:
        m_id = m_id2

    print(m_id)

    if request.method == "POST":

        profile_name = request.form.get("profile_name")

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()

        # Redirect user to home page
        return render_template("movie.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        print(m_id)

        connection = sqlite3.connect("netflix.db")
        connection.row_factory = sqlite3.Row
        db = connection.cursor()
        read = "SELECT * FROM movies WHERE movie_id = ?"
        db.execute(read, [m_id])
        movies = db.fetchone()

        print(movies)

        return render_template("movie.html", movies=movies)


@app.route("/show", methods=["GET"])
@login_required
def show():

    global m_id

    print(m_id)

    connection = sqlite3.connect("netflix.db")
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
    read = "SELECT * FROM movies WHERE movie_id = ?"
    db.execute(read, [m_id])
    movies = db.fetchone()

    print(movies)
    return render_template("show.html", movies=movies)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


