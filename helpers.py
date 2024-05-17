from flask import redirect, session
from functools import wraps
import requests
import langcodes


LIMIT = 20


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


def get_lang_names(lang_codes):
    lang = []
    for lang_code in lang_codes:
        lang.append(langcodes.get(lang_code).display_name())
    return lang


def query_books(params, url=None, key="docs"):
    if not url:
        url = "https://openlibrary.org/search.json"
    cover_url = "https://covers.openlibrary.org/b/id/"
    preview_url = 'https://openlibrary.org/books'
    payload = {
        "item_count": 0,
    }

    try:
        books = []
        res = requests.get(url, params)
        if res.status_code == 200:
            data = res.json()
            for doc in data.get(key):
                cover_id = doc.get("cover_i")
                id = doc.get("cover_edition_key",
                             doc.get("key").split("/")[-1])
                books.append({
                    "id": id,
                    "author_name": doc.get("author_name"),
                    "title": doc.get("title"),
                    "publish_year": doc.get("publish_year"),
                    "languages": doc.get("language"),
                    "edition_count": doc.get("edition_count"),
                    "cover_id": doc.get("cover_i"),
                    "image": f"{cover_url}{cover_id}-L.jpg" if cover_id else None,
                    "url": f"{preview_url}/{id}",
                })
            payload["books"] = books
            if key == "works":
                payload["item_count"] = data.get("days", 0)
            else:
                payload["item_count"] = data.get("numFound", 0)

        return payload
    except (KeyError, IndexError, requests.RequestException, ValueError) as e:
        print(e)
        return payload


def query_location(locations, offset):
    data = {}
    books = []
    cover_url = "https://covers.openlibrary.org/b/id/"
    for loc in locations[offset:offset+LIMIT]:
        book_id = loc['book_id']
        url = f'https://openlibrary.org/books/{book_id}.json'
        try:
            res = requests.get(url)
            if res.status_code == 200:
                payload = res.json()
                covers = data.get("covers")
                books.append({
                    "book_id": book_id,
                    "author_name": payload.get(""),
                    "title": payload.get("title"),
                    "description": payload.get("description"),
                    "url": url.split('.json')[0],
                    "image": f"{cover_url}{covers[0]}-L.jpg" if covers else None
                })
        except (KeyError, IndexError, requests.RequestException, ValueError) as e:
            print(e)

    data["books"] = books
    data["item_count"] = len(locations)
    return data
