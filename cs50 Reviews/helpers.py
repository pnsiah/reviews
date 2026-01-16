import requests
from flask import redirect, render_template, session
from functools import wraps
import os
from dotenv import load_dotenv

load_dotenv()


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


BASE_URL = "https://api.themoviedb.org/3"
IMG_URL = "https://image.tmdb.org/t/p/w500"
API_KEY = os.getenv("API_KEY")

popular_url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&sort_by=popularity"
trending_url = f"{BASE_URL}/trending/movie/week?api_key={API_KEY}"
movie_list_url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
tv_list_url = f"{BASE_URL}/genre/tv/list?api_key={API_KEY}&language=en-US"


def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def fetch_genre_data(type, id, page):
    url = f"{BASE_URL}/discover/{type}?api_key={API_KEY}&with_genres={id}&page={page}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


movie_genre_list = fetch_data(movie_list_url)
tv_genre_list = fetch_data(tv_list_url)


def movie_lookup(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def tv_lookup(movie_id):
    url = f"{BASE_URL}/tv/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def rating_to_stars(rating):
    stars = rating / 2
    full_stars = int(stars)
    remainder = stars - full_stars
    star_list = ["full"] * full_stars
    if remainder >= 0.25:
        star_list.append("half")
    empty_stars = 5 - len(star_list)
    star_list.extend(["empty"] * empty_stars)
    return star_list


def movie_search_lookup(search_term, page):
    # url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={search_term}&page={
    #     page
    # }&language=en"
    # url = f"{BASE_URL}/search/movie?api_key={API_KEY}&query={search_term}&page={
    #     page
    # }&language=en"
    url = (
        f"{BASE_URL}/search/movie?"
        f"api_key={API_KEY}&query={search_term}&page={page}&language=en"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def tv_search_lookup(search_term, page):
    # url = f"{BASE_URL}/search/tv?api_key={API_KEY}&query={search_term}&page={
    #     page
    # }&language=en"
    url = (
        f"{BASE_URL}/search/tv?"
        f"api_key={API_KEY}&query={search_term}&page={page}&language=en"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def multi_search_lookup(search_term, page):
    # url = f"{BASE_URL}/search/multi?api_key={API_KEY}&query={search_term}&page={
    #     page
    # }&language=en"
    url = (
        f"{BASE_URL}/search/multi?"
        f"api_key={API_KEY}&query={search_term}&page={page}&language=en"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        movie_data = response.json()
        return movie_data
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None
