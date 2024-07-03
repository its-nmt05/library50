# Library50

<p align="center">
  <img src="static/logo-light.svg">
</p>

**Video Demo:** https://youtu.be/-gMBYMm3IUc \
**Github:** https://github.com/its-nmt05/library50 \
**Description:** Library50 is a simple webapp that provides access to multiple books along with the ability to search them. The data is provided by [**Open library**](https://openlibrary.org/).

## Features

- **Extensive Book Database:** Access detailed information on millions of books, including titles, authors, publication dates, and ISBN numbers.
- **Search Functionality:** Easily search for books by title, author, subject, or ISBN using our intuitive search bar.
- **Book Details:** View comprehensive book details, including summaries, cover images, and links to borrow or purchase.
- **User-Friendly Interface:** Enjoy a clean and easy-to-navigate interface designed to enhance your browsing and reading experience.

## Tech stack

- **Flask:** A micro web framework for Python, known for its simplicity and flexibility, which allows us to build a robust and scalable web application.
- **Open Library API:** An open and editable library catalog that provides a wealth of information about books, authors, and publishers, making it an invaluable resource for our project.
- **HTML/CSS/JavaScript:** Standard web technologies used to create a responsive and interactive user interface.

## Files Description

`/app.py` - is the main
`/helpers.py` - it contains many helper functions used in `app.py` file:

- `login_required` to ensure that user is logged in for accessing some routes
- `get_lang_names` to get language name from codes
- `query_books` to get information from open for querying books
- `query_location` to get books stored in read-later and collections list from `stored` table

`/data.db` - contains two tables named `usrers` and `stored`. The first stores list of registered users and their password hashes.

The second one stores book_id's stored in user's collections or read-later lists.
`/requiremts.txt` - stores the required dependencies(python libraries) that need to be installed for the build
`/static/` - stores static files. It contains CSS stylesheets and images that are required for the front-end of the web application.

    /static/
        ├── book-thumbnail.png
        ├── favicon.ico
        ├── logo-small.svg
        ├── logo.svg
        ├── no-data.svg
        └── styles.css

`/templates/` - folder contains HTML template files used by Flask's rendering engine. These templates are dynamically rendered on the server side.

       /templates/
            ├── about.html
            ├── book-list.html
            ├── collections.html
            ├── index.html
            ├── layout.html
            ├── login.html
            ├── read-later.html
            ├── register.html
            └── trending.html

- `about.html` - Information about the application.
- `book-list.html` - Reusable book list display.
- `collections.html` - User's saved book collections.
- `index.html` - Main landing and search page.
- `layout.html` - Provides a consistent structure for all pages.
- `login.html` - User login form.
- `read-later.html` - Books marked to read later.
- `register.html` - User registration form.
- `trending.html` - List of trending books.

## Routes

#### Authentication Routes

- **Register (`/register`):** Handles user registration via GET and POST methods.
- **Login (`/login`):** Handles user login via GET and POST methods.
- **Logout (`/logout`):** Logs the user out by clearing the session.

#### Book Management Routes

- **Home (`/`):** Main page where users can search for books.
- **Trending (`/trending`):** Displays a list of trending books.
- **Collections (`/collections`):** Shows the user's saved book collections.
- **Read Later (`/read-later`):** Displays books saved for later reading.
- **Add Book (`/add`):** Allows users to add or remove books from their collections.

#### Other Routes

- **About (`/about`):** Displays information about the application.

## Database

The application uses SQLite, with a database named `data.db`, managed through the `cs50` SQL module. The following tables store all info:

- **`users`** stores user information (id, username, password hash).
- **`saved`** stores user-specific book data (user_id, book_id, location).

## Dependencies

- cs50
- Flask
- Flask-Session
- langcodes
- requests

## Security

- **Password Hashing:** Passwords are securely hashed using `werkzeug.security`.
- **Session Protection:** Ensures responses are not cached to protect user data.

## Running the Application

To run the application, execute the following command:
`python app.py`

By default, the application will run on `http://localhost:5000` with debug mode enabled.

## Acknowledgements

I would like to thank the following for their support and resources:

- **cs50:** For providing the foundational knowledge and support to undertake this project.
- **Open Library:** For their extensive API and commitment to making book information accessible to all.
- **Flask Community:** For the comprehensive documentation and community support that made development a smooth process.

Thank you for visiting Library50. I hope you find it useful and inspiring. Happy reading!
