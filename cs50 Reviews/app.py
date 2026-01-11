import os
from datetime import datetime
from cs50 import SQL
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
import sqlite3
import secrets
from PIL import Image
from helpers import (
    login_required,
    apology,
    fetch_data,
    popular_url,
    trending_url,
    movie_genre_list,
    tv_genre_list,
    fetch_genre_data,
    movie_lookup,
    tv_lookup,
    rating_to_stars,
    tv_search_lookup,
    movie_search_lookup,
    multi_search_lookup,
)

app = Flask(__name__)

# Session configuration to filesystem
app.config["SESSION_PERMAMENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


@app.after_request
def add_no_cache_headers(response):
    response.cache_control.no_store = True
    response.cache_control.must_revalidate = True
    return response


# Available to all templates


@app.context_processor
def inject_user_data():
    return dict(user_data=session.get("user_data"))


# Custom filter for year extraction


def format_year(date_str):
    if not date_str:
        return "No Date Provided"
    try:
        # Adjust the format to match "year-month-day"
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.year
    except ValueError:
        return "Invalid Date"


# Register the filter
app.jinja_env.filters["format_year"] = format_year

# global variables


@app.context_processor
def inject_globals():
    return {
        "BASE_URL": "https://api.themoviedb.org/3",
        "IMG_URL": "https://image.tmdb.org/t/p/original",
    }


Session(app)

# Database configuration
db = SQL("sqlite:///site.db")


@app.route("/", methods=["POST", "GET"])
@login_required
def home():
    if request.method == "GET":
        trending_movies = fetch_data(trending_url)
        popular_movies = fetch_data(popular_url)
        return render_template(
            "/home.html", popular_movies=popular_movies, trending_movies=trending_movies
        )


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        # collect user info
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")
        # validate user input
        if not username:
            return apology("Username must be provided", 400)
        if not email:
            return apology("Enter email", 400)
        elif not password:
            return apology("Enter your password", 400)
        elif not confirm_password:
            return apology("Confirm password", 400)
        elif not password == confirm_password:
            return apology("Passwords do not match", 400)
        # Hash password
        hashed_password = generate_password_hash(password)
        # Insert user into db
        try:
            db.execute(
                "INSERT INTO users(username, email, password) VALUES (?,?,?)",
                username,
                email,
                hashed_password,
            )
            # redirect to login page
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return apology("Username already exists", 400)
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("Must provide email", 400)
        elif not request.form.get("password"):
            return apology("Must provide password", 400)
        # Query database for email
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )
        # Ensure email exists and passwoord is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password"], request.form.get("password")
        ):
            return apology("Invalid username and/or password", 400)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_data"] = {
            "username": rows[0]["username"],
            "email": rows[0]["email"],
            "image_file": rows[0]["image_file"],
        }
        flash("You've logged in successfully", "success")
        # Redirect user to home page
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    # Log out user
    session.clear()
    return redirect(url_for("login"))


@app.route("/movie", methods=["GET", "POST"])
@login_required
def movie():
    return render_template("movie.html", genres=movie_genre_list["genres"])


@app.route("/tv", methods=["GET", "POST"])
@login_required
def tv():
    print(movie_genre_list)
    return render_template("tv.html", genres=tv_genre_list["genres"])


@app.route("/movie/<id>", methods=["GET", "POST"])
@login_required
def movie_item(id):
    if request.method == "GET":
        movie_data = movie_lookup(id)
        stars = rating_to_stars(movie_data["vote_average"])
        try:
            # Correct SQL Query
            reviews = db.execute(
                """SELECT 
                (SELECT username FROM users WHERE id = movie_reviews.author_id) AS username, 
                (SELECT image_file FROM users WHERE id = movie_reviews.author_id) AS profile_pic, 
                title, 
                content, 
                created_at 
            FROM movie_reviews WHERE movie_id = ?""",
                id,
            )
            return render_template(
                "movie_item.html", movie_data=movie_data, stars=stars, reviews=reviews
            )
        except ValueError:
            return apology("Error getting values", 400)
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not title:
            return apology("Title must not be empty")
        if not content:
            return apology("Content must not be empty")
        try:
            # insert data into the movie_reviews table
            db.execute(
                "INSERT INTO movie_reviews (author_id, movie_id, title, content)VALUES(?, ?, ?, ?)",
                session["user_id"],
                id,
                title,
                content,
            )
        except ValueError:
            return apology("Error entering in values", 400)
        flash("Review added successfully", "success")
        return redirect(url_for("movie_item", id=id))


@app.route("/tv/<id>", methods=["GET", "POST"])
@login_required
def tv_item(id):
    if request.method == "GET":
        # Assuming tv_lookup is a function to get TV show details
        movie_data = tv_lookup(id)
        # Convert rating to stars
        stars = rating_to_stars(movie_data["vote_average"])
        try:
            # SQL query to fetch reviews for the TV show
            reviews = db.execute(
                """SELECT 
                    (SELECT username FROM users WHERE id = tv_reviews.author_id) AS username, 
                    (SELECT image_file FROM users WHERE id = tv_reviews.author_id) AS profile_pic, 
                    title, 
                    content, 
                    created_at 
                FROM tv_reviews WHERE tv_id = ?""",
                id,
            )
            return render_template(
                "tv_item.html",  # Assuming you're rendering a TV-specific template
                movie_data=movie_data,
                stars=stars,
                reviews=reviews,
            )
        except ValueError:
            return apology("Error getting values", 400)

    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        # Validate the form input
        if not title:
            return apology("Title must not be empty")
        if not content:
            return apology("Content must not be empty")
        try:
            # Insert the review into the tv_reviews table
            db.execute(
                "INSERT INTO tv_reviews (author_id, tv_id, title, content) VALUES (?, ?, ?, ?)",
                session["user_id"],
                id,
                title,
                content,
            )
        except ValueError:
            return apology("Error entering values", 400)
        # Flash a success message
        flash("Review added successfully", "success")
        # Redirect back to the current page
        return redirect(url_for("tv_item", id=id))


@app.route("/movie/<genre>/<int:id>")
@login_required
def movie_genre(genre, id):
    page = int(request.args.get("page", 1))
    results = fetch_genre_data("movie", id, page)
    return render_template(
        "movie_genre.html",
        movies=results,
        genre=genre,
        current_page=page,
        total_pages=results["total_pages"],
        id=id,
    )


@app.route("/tv/<genre>/<int:id>")
@login_required
def tv_genre(genre, id):
    page = int(request.args.get("page", 1))
    results = fetch_genre_data("tv", id, page)
    return render_template(
        "tv_genre.html",
        movies=results,
        genre=genre,
        current_page=page,
        total_pages=results["total_pages"],
        id=id,
    )


def save_pic(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pictures", picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "GET":
        return render_template("profile.html")
    if request.method == "POST":
        new_username = request.form.get("username")
        new_email = request.form.get("email")
        profile_pic = request.files.get("profile_pic")
        if not new_username:
            return apology("Enter username", 400)
        if not new_email:
            return apology("Enter email", 400)

        if (
            new_email != session["user_data"]["email"]
            or new_username != session["user_data"]["username"]
        ):
            if new_email != session["user_data"]["email"]:
                try:
                    db.execute(
                        "UPDATE users SET email = ? WHERE id = ?",
                        new_email,
                        session["user_id"],
                    )
                    session["user_data"]["email"] = new_email
                except sqlite3.IntegrityError:
                    return apology("Email is taken", 400)
            if new_username != session["user_data"]["username"]:
                try:
                    db.execute(
                        "UPDATE users SET username = ? WHERE id = ?",
                        new_username,
                        session["user_id"],
                    )
                    session["user_data"]["username"] = new_username
                except sqlite3.IntegrityError:
                    return apology("Username is taken", 400)
            flash("Profile updated sucessfully", "success")
        elif profile_pic:
            profile_fn = save_pic(profile_pic)
            db.execute(
                "UPDATE users SET image_file = ? WHERE id = ?",
                profile_fn,
                session["user_id"],
            )
            session["user_data"]["image_file"] = profile_fn
            flash("Profile picture updated successfully", "success")
        else:
            flash("No changes detected", "warning")
        return redirect(url_for("profile"))


@app.route("/movie_search", methods=["POST", "GET"])
@login_required
def movie_search():
    if request.method == "POST":
        # Process the form submission
        search_term = request.form.get("search_term")

        if not search_term:
            flash("Please enter a search term.", "warning")
            return redirect(url_for("movie"))
        # Store the search term in the session
        session["search_term"] = search_term
        # Redirect to the same route for results
        return redirect(url_for("movie_search"))

    # Handle the GET request to display results
    search_term = session.get("search_term", None)

    if not search_term:
        # If no search term exists, redirect back to the form
        return redirect(url_for("movie"))

    # Perform the movie search lookup
    page = int(request.args.get("page", 1))
    movies = movie_search_lookup(search_term, page)

    # Render the results page
    return render_template(
        "movie_search.html",
        movies=movies,
        search_term=search_term,
        current_page=page,
        total_pages=movies["total_pages"],
    )


@app.route("/tv_search", methods=["POST", "GET"])
@login_required
def tv_search():
    if request.method == "POST":
        # Process the form submission
        search_term = request.form.get("search_term")

        if not search_term:
            flash("Please enter a search term.", "warning")
            return redirect(url_for("tv"))

        # Store the search term in the session
        session["search_term"] = search_term

        # Redirect to the same route for results
        return redirect(url_for("tv_search"))

    # Handle the GET request to display results
    search_term = session.get("search_term", None)

    if not search_term:
        # If no search term exists, redirect back to the form
        return redirect(url_for("tv"))

    page = int(request.args.get("page", 1))
    # Perform the movie search lookup
    movies = tv_search_lookup(search_term, page)

    # Render the results page
    return render_template(
        "tv_search.html",
        movies=movies,
        search_term=search_term,
        current_page=page,
        total_pages=movies["total_pages"],
    )


@app.route("/multi_search", methods=["POST", "GET"])
@login_required
def multi_search():
    if request.method == "POST":
        # Process the form submission
        search_term = request.form.get("search_term")

        if not search_term:
            flash("Please enter a search term.", "warning")
            return redirect(url_for("home"))

        # Store the search term in the session
        session["search_term"] = search_term

        # Redirect to the same route for results
        return redirect(url_for("multi_search"))

    # Handle the GET request to display results
    search_term = session.get("search_term", None)

    if not search_term:
        # If no search term exists, redirect back to the form
        return redirect(url_for("home"))

    page = int(request.args.get("page", 1))
    # Perform the movie search lookup
    movies = multi_search_lookup(search_term, page)

    # Render the results page
    return render_template(
        "multi_search.html",
        movies=movies,
        search_term=search_term,
        current_page=page,
        total_pages=movies["total_pages"],
    )


if __name__ == "__main__":
    app.run(debug=True)
