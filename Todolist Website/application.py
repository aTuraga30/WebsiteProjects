from cs50 import SQL

from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

# Configures the Flask App
app = Flask(__name__)

# Sets a secret key for the application
app.config["SECRET_KEY"] = '52ee0e2a4938f9c3c84094693a4a9d5b95c5'

# FROM CS50 - Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# FROM CS50 - Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# FROM CS50 - Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Sets the database for the login page, this is from CS50
db = SQL("sqlite:///users.db")

# Sets a database table - This is only done once
# db.execute("CREATE TABLE Users (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)")
# db.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, task TEXT NOT NULL, status TEXT NOT NULL)")


@app.route("/")
@app.route("/page")
def page():
    return render_template("page.html", title="Home")


@app.route("/test")
def test():
    return render_template("test.html")


# ---------------------------------------------------------------------------------------------------------------------------------
@app.route("/base")
@login_required
def base():

    todo = db.execute("SELECT task, status FROM todo WHERE user_id = :user_id", user_id=session["user_id"])
    return render_template("base.html", todo=todo)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":

        if not request.form.get("task"):
            return render_template("apology.html", message="Please enter a valid task")

        db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
                   task=request.form.get("task"), status="Not Completed")

        return redirect(url_for("base"))

    else:
        return render_template("add.html")


@app.route("/update", methods=["GET", "POST"])
@login_required
def update():

    if request.method == "POST":

        if request.form.get("task") == "" or '':
            return render_template("apology.html", message="Please enter a valid task")

        db.execute("UPDATE todo SET status = :status WHERE task = :task AND user_id = :user_id", status="Completed", task=request.form.get("task"),
                   user_id=session["user_id"])

        return redirect(url_for("base"))

    else:
        todos = db.execute("SELECT task, status FROM todo WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("update.html", todos=todos)


@app.route("/revert", methods=["GET", "POST"])
@login_required
def revert():

    if request.method == "POST":

        if request.form.get("revert") == "" or '':
            return render_template("apology.html", message="Please enter a valid task")

        db.execute("UPDATE todo SET status = :status WHERE task = :task AND user_id = :user_id", status="Not Completed",
                   task=request.form.get("revert"), user_id=session["user_id"])

        return redirect(url_for("base"))

    else:
        todos = db.execute("SELECT task, status FROM todo WHERE status = :status AND user_id = :user_id",
                           status="Completed", user_id=session["user_id"])

        return render_template("revert.html", todos=todos)


@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():

    if request.method == "POST":

        if request.form.get("delete") == "" or '':
            return render_template("apology.html", message="Please enter a valid task to delete")

        db.execute("DELETE FROM todo WHERE task = :task AND user_id = :user_id", task=request.form.get("delete"), user_id=session["user_id"])

        return redirect(url_for("base"))

    else:
        todos = db.execute("SELECT task FROM todo WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("delete.html", todos=todos)

# ------------------------------------------------------------------------------------------------------


@app.route("/morning")
@login_required
def morning():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Workout for 45 minutes"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Create a morning routine", status="Not Completed")

    return redirect("/base")


@app.route("/workout")
@login_required
def workout():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Workout for 45 minutes"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Try a new workout", status="Not Completed")

    return redirect("/base")


@app.route("/meditate")
@login_required
def meditate():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Meditate for 10 minutes"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Meditate for 10 minutes", status="Not Completed")

    return redirect("/base")


@app.route("/grat")
@login_required
def grat():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Take 10 minutes to show gratitude"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Take 10 minutes to show gratitude", status="Not Completed")

    return redirect("/base")


@app.route("/lem")
@login_required
def lem():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Drink a glass of lemon water"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Drink a glass of lemon water", status="Not Completed")

    return redirect("/base")


@app.route("/walk")
@login_required
def walk():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Walk for 15 minutes"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Walk for 15 minutes", status="Not Completed")

    return redirect("/base")


@app.route("/time")
@login_required
def time():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Identify areas where you can manage time"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Identify areas where you can manage time", status="Not Completed")

    return redirect("/base")


@app.route("/read")
@login_required
def read():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Read for 30 minutes"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Read for 30 minutes", status="Not Completed")

    return redirect("/base")


@app.route("/tidy")
@login_required
def tidy():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Make sure that your workspace is tidy"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Make sure that your workspace is tidy", status="Not Completed")

    return redirect("/base")


@app.route("/pos")
@login_required
def pos():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Take 10 minutes to think positively"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Take 10 minutes to think positively", status="Not Completed")

    return redirect("/base")


@app.route("/sleep")
@login_required
def sleep():

    if db.execute("SELECT * FROM todo WHERE user_id = :user_id AND task = :task", user_id=session["user_id"], task="Try to sleep for 7 to 8 hours tonight"):
        return render_template("apology.html", message="Task is already in todo list")

    db.execute("INSERT INTO todo (user_id, task, status) VALUES (:user_id, :task, :status)", user_id=session["user_id"],
               task="Try to sleep for 7 to 8 hours tonight", status="Not Completed")

    return redirect("/base")

#---------------------------------------------------------------------------------------------------------------------------------


@app.route("/home")
@login_required
def home():
    return render_template("home.html", title="Home")

# ---------------------------------------------------------------------------------------------------------------------------------

# This is route "login", and the code in this route takes care of everything you need to login to the app


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return render_template("apology.html", message="Please enter a valid username")

        elif not password:
            return render_template("apology.html", message="Please enter a valid password")

        # Sets the database again to avoid further errors
        db = SQL("sqlite:///users.db")

        # Gets the entered username from the database
        check = db.execute("SELECT * FROM Users WHERE username = :username", username=request.form.get("username"))

        # Checks to see if the password is correct for the given username
        if len(check) != 1 or not check_password_hash(check[0]["password"], request.form.get("password")):
            return render_template("apology.html", message="Sorry, invalid username or password")

        # Sets the session
        session["user_id"] = check[0]["id"]

        flash("Logged in!")
        return redirect("/home")
    # If the method is a "get", which means to get information, then it will render the html document
    else:
        return render_template("login.html")
# ----------------------------------------------------------------------------------------------------------------------------------


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        db = SQL("sqlite:///users.db")

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return render_template("apology.html", message="Please enter a valid username")

        elif not password:
            return render_template("apology.html", message="Please enter a valid password")

        elif not confirmation:
            return render_template("apology.html", message="Please enter a valid password confirmation")

        elif password != confirmation:
            return render_template("apology.html", message="Please make sure your passwords match")

        elif db.execute('SELECT * FROM Users WHERE username = :username', username=request.form.get("username")):
            return render_template("apology.html", message="Sorry, the username is already taken")

        hash = generate_password_hash(password)

        db.execute("INSERT INTO Users (username, password) VALUES (:username, :password) ",
                   username=request.form.get("username"), password=hash)

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/web")
def web():
    return render_template("web.html", title="Web Stats")
# ----------------------------------------------------------------------------------------------------------------------------------


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -----------------------------------------------------------------------------------------------------------------------------------
# All this code handles any errors
if __name__ == "__main__":
    app.run(debug=True)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return e.name, e.code


for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
# -------------------------------------------------------------------------------------------------------------------------------------
