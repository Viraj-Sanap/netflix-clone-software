import sqlite3
from flask import redirect, render_template, request, session, flash
from functools import wraps


def create_table():
    connection = sqlite3.connect('netflix.db')
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'users'('username' TEXT NOT NULL UNIQUE, 'password' TEXT NOT NULL,"
                   "PRIMARY KEY('username'))")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'profile'('p_id' INTEGER NOT NULL UNIQUE, 'p_name' TEXT NOT NULL, "
                   "'username' TEXT NOT NULL, PRIMARY KEY('p_id' AUTOINCREMENT)"
                   "FOREIGN KEY('username') REFERENCES 'users'('username') on delete cascade on update cascade)")
    cursor.execute("CREATE TABLE IF NOT EXISTS 'movies'('movie_id' TEXT NOT NULL UNIQUE, 'movie_name' TEXT NOT NULL,"
                   "'desc' TEXT NOT NULL, 'cast' TEXT NOT NULL, 'img' TEXT NOT NULL, 'synopsis' TEXT NOT NULL,"
                   "'img2' TEXT NOT NULL, 'video' TEXT NOT NULL, 'type' TEXT NOT NULL, PRIMARY KEY('movie_id'))")


'''
    cursor.execute("CREATE TABLE IF NOT EXISTS 'students'('s_id' TEXT NOT NULL, 'student_name' TEXT NOT NULL,"
                   "'prof' INTEGER NOT NULL, 'div' TEXT NOT NULL, PRIMARY KEY('div', 's_id') FOREIGN KEY(prof) "
                   "references prof(id) on delete cascade on update cascade)")

    cursor.execute("CREATE TABLE IF NOT EXISTS 'attendance'('a_id' INTEGER NOT NULL UNIQUE, 'date' TEXT NOT NULL, "
                   "'stu_div' TEXT NOT NULL, 'stud_id' TEXT NOT NULL, 'status' TEXT NOT NULL, "
                   "PRIMARY KEY('a_id' AUTOINCREMENT), "
                   "FOREIGN KEY('stu_div') REFERENCES 'students'('div') on delete cascade on update cascade, "
                   "FOREIGN KEY('stud_id') REFERENCES 'students'('s_id') on delete cascade on update cascade)")
'''


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/main")
        return f(*args, **kwargs)

    return decorated_function


def apology_exists():
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    message = "true"
    return render_template("signup.html", top_ex=message)


def apology_match():
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    message = "true"
    return render_template("signup.html", top=message)


def apology_login():
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    message = "true"
    return render_template("login.html", top=message)


def apology_login2():
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    message = "true"
    return render_template("login.html", top2=message)
