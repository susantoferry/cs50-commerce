# Commerce

An eBay-style auction site built with Django for CS50's Web Programming with Python and JavaScript (Project 2). Users can post listings, bid, comment, keep a watchlist, browse by category, and get notified when an auction they bid on closes.

The data is stored in **MongoDB** through [django-mongodb-backend](https://github.com/mongodb/django-mongodb-backend).

## Requirements

- Python 3.10 or newer
- A MongoDB database, either:
  - **MongoDB Atlas** (free cloud cluster): create one at <https://www.mongodb.com/cloud/atlas>, add a database user, and allow your IP under *Network Access*; or
  - **Local MongoDB 6.0+**, for example with Docker:
    ```bash
    docker run -d --name commerce-mongo -p 27017:27017 mongo:8
    ```

## Setup

1. **Clone the repository and create a virtual environment**

   ```bash
   git clone <repo-url> commerce
   cd commerce
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure the database connection**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set `MONGODB_URI`:

   ```
   # Atlas
   MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/
   # or local
   MONGODB_URI=mongodb://localhost:27017/
   ```

   The app uses a database named `commerce`; it is created automatically. `.env` is git-ignored, so your credentials stay local.

3. **Create the collections**

   ```bash
   python manage.py migrate
   ```

4. **Load the sample data** (optional, but recommended)

   ```bash
   python manage.py import_sqlite      # copies users, categories, auctions, bids, etc. from db.sqlite3
   python manage.py create_demo_users  # makes the demo accounts below usable
   ```

   `import_sqlite` refuses to run if the database already has auctions, so it is safe to run once. If you skip it, `create_demo_users` still creates the four accounts, but there will be no listings.

5. **Run the server**

   ```bash
   python manage.py runserver
   ```

   Open <http://127.0.0.1:8000/>.

## Demo accounts

These are also listed on the login page. Log in with the **username** (not the email).

| Username | Password |
|---|---|
| ferry | password |
| keele | password |
| stacy | password |
| chris | password |

`ferry` is a superuser, so it can also sign in to the admin site at <http://127.0.0.1:8000/admin/>. To create your own admin account instead, run `python manage.py createsuperuser`.

## Listing images

A listing's image is either an external URL (entered when posting the listing) or an image file stored in MongoDB. To store a file for an existing auction:

```bash
# find the auction's id
python manage.py shell -c "from auctions.models import Auction; [print(a.id, a.title) for a in Auction.objects.all()]"

# attach the image (jpg, png, webp, ...)
python manage.py attach_image 6abba7fef9c68d961b5041ad ~/Downloads/laptop.jpg
```

Stored images are served from `/auction-image/<auction id>`.

## Management commands

| Command | What it does |
|---|---|
| `import_sqlite [--path FILE]` | Copies the data from `db.sqlite3` (the app's original database) into MongoDB. |
| `create_demo_users` | Creates the demo accounts, or resets their passwords to `password`. |
| `attach_image <auction_id> <file>` | Stores an image file in MongoDB and uses it as the auction's picture. |

## Troubleshooting

- **`KeyError: 'MONGODB_URI'`**: `.env` is missing or doesn't set `MONGODB_URI` (see step 2).
- **`ServerSelectionTimeoutError`**: the app can't reach MongoDB. For Atlas, check that your current IP is allowed under *Network Access* and the user/password in the URI are correct. For local MongoDB, check the server or container is running.
- **`ModuleNotFoundError: No module named 'django'`**: the virtual environment isn't active. Run `source venv/bin/activate`, or call `venv/bin/python manage.py ...` directly (this also works with `sudo`).
- **"Invalid username and/or password"**: use the username, not the email, and run `python manage.py create_demo_users` if the demo accounts don't work.
