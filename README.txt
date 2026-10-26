LITTLE LEMON - DJANGO REST FRAMEWORK CAPSTONE
=============================================

OVERVIEW
--------
This project demonstrates a Django restaurant backend with:
- Django serving a simple static HTML homepage.
- Menu API (list, create, retrieve, update, delete).
- Table booking API (list, create, retrieve, update, delete).
- User registration and token authentication.
- MySQL database configuration.
- Automated unit tests.
- Endpoints that can be tested using Insomnia.

REQUIREMENTS
------------
Python 3.10+ recommended
MySQL Server 8+ for the MySQL configuration
Git and VS Code

SETUP
-----
1. Extract the ZIP and open the project folder in VS Code.

2. Create and activate a virtual environment:
   Windows:
     py -m venv .venv
     .venv\Scripts\activate
   macOS/Linux:
     python3 -m venv .venv
     source .venv/bin/activate

3. Install dependencies:
     pip install -r requirements.txt

4. Configure database credentials:
   Copy .env.example to .env and set your MySQL credentials.
   This project reads environment variables directly; if you do not use a
   .env loader, set the variables in your terminal before running Django.

   Windows PowerShell example:
     $env:DB_NAME="littlelemon"
     $env:DB_USER="littlelemon_user"
     $env:DB_PASSWORD="your-password"
     $env:DB_HOST="127.0.0.1"
     $env:DB_PORT="3306"
     $env:DJANGO_SECRET_KEY="replace-with-a-secret"
     $env:DJANGO_DEBUG="True"

   Create the database and user in MySQL (adjust password as needed):
     CREATE DATABASE littlelemon CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     CREATE USER 'littlelemon_user'@'localhost' IDENTIFIED BY 'your-password';
     GRANT ALL PRIVILEGES ON littlelemon.* TO 'littlelemon_user'@'localhost';
     FLUSH PRIVILEGES;

   Quick SQLite alternative (for a first smoke test only):
     Windows PowerShell: $env:DB_ENGINE="sqlite"
     macOS/Linux: export DB_ENGINE=sqlite

5. Create database tables and start the server:
     python manage.py makemigrations restaurant
     python manage.py migrate
     python manage.py createsuperuser
     python manage.py runserver

6. Open:
     http://127.0.0.1:8000/

ADMIN
-----
Admin dashboard: http://127.0.0.1:8000/admin/

API ENDPOINTS TO TEST IN INSOMNIA
---------------------------------
Homepage:
  GET     http://127.0.0.1:8000/

Authentication:
  POST    http://127.0.0.1:8000/api/auth/register/
          JSON: {"username":"demo","email":"demo@example.com","password":"StrongPass123!"}
  POST    http://127.0.0.1:8000/api/auth/token/
          JSON: {"username":"demo","password":"StrongPass123!"}
          Copy the returned token for authenticated requests.

Menu:
  GET     http://127.0.0.1:8000/api/menu/
  POST    http://127.0.0.1:8000/api/menu/
  GET     http://127.0.0.1:8000/api/menu/1/
  PUT     http://127.0.0.1:8000/api/menu/1/
  PATCH   http://127.0.0.1:8000/api/menu/1/
  DELETE  http://127.0.0.1:8000/api/menu/1/

Bookings:
  GET     http://127.0.0.1:8000/api/bookings/
  POST    http://127.0.0.1:8000/api/bookings/
  GET     http://127.0.0.1:8000/api/bookings/1/
  PUT     http://127.0.0.1:8000/api/bookings/1/
  PATCH   http://127.0.0.1:8000/api/bookings/1/
  DELETE  http://127.0.0.1:8000/api/bookings/1/

For POST /api/menu/:
  {"title":"Greek Salad","price":"12.50","inventory":20}

For POST /api/bookings/:
  {"name":"Alex Morgan","no_of_guests":2,"booking_date":"2026-11-01T19:00:00Z"}

AUTHENTICATION NOTES
--------------------
Registration is public. Menu and booking read endpoints are public; creating,
updating, and deleting menu items or bookings requires a valid DRF token.
For protected requests add header:
  Authorization: Token YOUR_TOKEN_HERE
Use Content-Type: application/json for JSON requests.

TESTS
-----
Run:
  python manage.py test

GIT / GITHUB SUBMISSION
-----------------------
Initialize and push the project:
  git init
  git add .
  git commit -m "Build Little Lemon Django REST API capstone"
  git branch -M main
  git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
  git push -u origin main

Then submit the GitHub repository URL in Coursera's My submission tab.
This ZIP does not create or push a GitHub repository automatically.

IMPORTANT
---------
For a graded submission, run the app, verify the MySQL connection, run the tests,
and test the endpoints in Insomnia before submitting. Do not claim that these
checks passed until you have run them in your environment.
