from cs50 import SQL
from flask_session import Session
from flask import Flask, redirect, render_template, flash, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, get_lang_names, query_books, query_location, LIMIT

# configure application
app = Flask(__name__)

# connect to database (data.db)
db = SQL("sqlite:///data.db")

# setup jinja functions
app.jinja_env.filters['get_lang_names'] = get_lang_names

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    query = request.args.get("query")
    filter = request.args.get("filter")
    page = request.args.get("page", "1")
    offset = 0

    if page.isdigit():
        offset = (int(page) - 1) * LIMIT
    else:
        page = 0

    data = {}
    if query and filter:
        data["filter"] = filter
        data["query"] = query
        if filter == "all":
            filter = "q"
        params = {
            filter: query,
            "offset": offset,
            "page": int(page),
        }
        data.update(params)
        data.update(query_books(params))
        data["total_pages"] = (data["item_count"] + LIMIT - 1) // LIMIT

    return render_template("index.html", data=data)


@app.route("/trending", methods=["GET"])
@login_required
def trending():
    page = request.args.get("page", "1")
    offset = 0
    data = {}

    if page.isdigit():
        offset = (int(page) - 1) * LIMIT
    else:
        page = 0

    params = {
        "offset": offset,
        "page": int(page),
    }
    data.update(params)
    data.update(query_books(
        params, url="https://openlibrary.org/trending/yearly.json", key="works"))

    data["total_pages"] = (data["item_count"] + LIMIT - 1) // LIMIT
    data["query"] = "Trending"
    return render_template("trending.html", data=data)


@app.route("/collections")
@login_required
def collections():
    page = request.args.get("page", "1")
    if page.isdigit():
        offset = (int(page) - 1) * LIMIT
    else:
        page = 0

    locs = db.execute(
        "SELECT book_id FROM saved WHERE user_id = ? AND location = ?",
        session["user_id"], "collection"
    )
    data = query_location(locs, offset)
    data["total_pages"] = (data["item_count"] + LIMIT - 1) // LIMIT
    data["query"] = "collections"
    data["page"] = int(page)
    data["offset"] = offset

    return render_template("collections.html", data=data)


@app.route("/read-later")
@login_required
def read_later():
    page = request.args.get("page", "1")
    if page.isdigit():
        offset = (int(page) - 1) * LIMIT
    else:
        page = 0

    locs = db.execute(
        "SELECT book_id FROM saved WHERE user_id = ? AND location = ?",
        session["user_id"], "read-later"
    )
    data = query_location(locs, offset)
    data["total_pages"] = (data["item_count"] + LIMIT - 1) // LIMIT
    data["query"] = "Read later"
    data["page"] = int(page)
    data["offset"] = offset

    return render_template("read-later.html", data=data)


@app.route("/register", methods=["GET", "POST"])
def register():

    # user has entered this route via POST action (submitting a form)
    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # form not submitted correctly
        if not username:
            flash('Missing username', 'warning')
            return render_template("register.html")

        if not password:
            flash('Missing password', 'warning')
            return render_template("register.html")

        if not confirmation:
            flash('Missing confirmation', 'warning')
            return render_template("register.html")

        if password != confirmation:
            flash("Passwords don't match", 'warning')
            return render_template("register.html")

        # check for user with same user-name
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", username
        )

        # user with same username already exists! redirect
        if len(rows) != 0:
            flash('Username already exists', 'warning')
            return render_template("register.html")

        # form submitted correctly (create new user)
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES(?, ?)",
            username, generate_password_hash(password)
        )

        # store the newly created user's id into the current session
        user_id = db.execute(
            "SELECT * FROM users WHERE username = ?", username)[0]["id"]

        session["user_id"] = user_id
        flash("Registered successfully", "success")
        return redirect("/")

    # user has entered this route via GET action (clicking on a link)
    else:
        if session.get("user_id"):
            return redirect("/")

        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # user has entered this route via POST action (submitting a form)
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            flash('Missing username', 'warning')
            return render_template("login.html")

        if not password:
            flash('Missing password', 'warning')
            return render_template("login.html")

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # check if username exists and apssword is valid
        if len(rows) != 1 or not check_password_hash(rows[0]["password_hash"], password):
            flash('Invalid username or password', 'warning')
            return redirect("/")

        session["user_id"] = rows[0]["id"]
        flash("Logged in successfully", "success")
        return redirect("/")

    # user has entered this route via GET action (clicking on a link)
    else:
        if session.get("user_id"):
            return redirect("/")

        return render_template("login.html")


@app.route("/add", methods=["POST"])
def add():
    book_id = request.form.get("book_id")
    loc = request.form.get("loc")

    if loc == "remove":
        db.execute(
            "DELETE FROM saved WHERE user_id = ? AND book_id = ?",
            session["user_id"], book_id
        )

    else:
        # save book id to location
        books = db.execute(
            "SELECT * FROM saved WHERE user_id = ? AND book_id = ? AND location = ?",
            session["user_id"], book_id, loc
        )

        if len(books) == 0:
            db.execute(
                "INSERT INTO saved (user_id, book_id, location) VALUES (?, ?, ?)",
                session["user_id"], book_id, loc
            )

    return "Add"


@app.route("/logout")
def logout():
    """clear current session"""
    session.clear()
    return redirect("/")


@app.route("/about")
@login_required
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
