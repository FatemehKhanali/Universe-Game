# Universe-Game

A Django-based web application for browsing, reviewing, purchasing, and downloading digital games.

Universe-Game was developed as my bachelor's final project using **Python and Django**. The project gave me practical experience in building a web application with Django, working with databases and ORM, authentication, sessions, shopping cart and order workflows, and basic authorization.

> **Project status:** Academic / portfolio project.
> This project is not presented as a production-ready e-commerce platform.

## Features

* User registration and login
* Email verification
* OTP-based login
* User profile management
* Game categories
* Game search
* Game details
* Reviews and ratings
* Session-based shopping cart
* Checkout workflow
* Order management
* Payment flow with a payment simulator
* Game download after a successful payment flow
* Django Admin
* Responsive frontend
* Basic chatbot functionality

## Backend Highlights

The project includes several backend concepts implemented with Django:

* Django ORM and database models
* Model relationships
* URL routing and views
* Forms and form handling
* User authentication and authorization
* Session management
* Shopping cart logic
* Checkout and order processing
* Access control for purchased games
* Django Admin

### Main Models

The main models include:

* `BaseModel`
* `Category`
* `Game`
* `Cart`
* `Order`
* `OrderGame`
* `PaymentLog`

The models use relationships between users, games, carts, orders, and order items.

`BaseModel` also provides common fields such as creation/update timestamps and a soft-delete flag.

## Payment Flow

The project includes an attempt to implement a payment flow similar to the **ZarinPal** payment process.

Since the real API integration was not completed, a **payment simulator** was designed and implemented to demonstrate the payment flow within the project.

The simulator provides a project-level payment experience and is intended for demonstration purposes. It is **not a real production payment gateway**.

## Authorization and Download

The download functionality includes basic authorization checks.

Before allowing a user to download a game, the application checks that:

* The game exists in an `OrderGame` record.
* The related order belongs to the current user.
* The order has been marked as paid.

This connects the purchasing workflow with access to purchased games.

## Search

The project includes a basic game search feature using Django ORM.

Users can search for games by title, and matching results can be opened through the game's detail page.

The search implementation is intentionally simple and is not intended to be an advanced search engine.

## Technologies

### Backend

* Python
* Django
* Django ORM
* SQLite

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

### Tools

* PyCharm
* Git
* GitHub

## Project Structure

```text
Universe-Game/
│
├── accounts/
│   └── Authentication and profile-related functionality
│
├── game_universe/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── settings.py
│   ├── cart.py
│   └── ...
│
├── manage.py
├── requirements.txt
├── .gitignore
└── .gitattributes
```

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/FatemehKhanali/Universe-Game.git
cd Universe-Game
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key
```

Do not commit the `.env` file to Git.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Check the project

```bash
python manage.py check
```

### 7. Start the development server

```bash
python manage.py runserver
```

The application will normally be available at:

```text
http://127.0.0.1:8000/
```

## Project Strengths

This project helped me gain practical experience with several important backend concepts, including:

* Building a web application with Django
* Designing database models and relationships
* Using Django ORM for database operations
* Implementing authentication and session management
* Managing carts, orders, and checkout workflows
* Implementing basic authorization and access control
* Working with Django Admin
* Connecting backend logic with a responsive frontend
* Managing configuration through environment variables

## Limitations and Future Improvements

As an academic project, there are areas that could be improved in a future version, including:

* Adding automated tests
* Improving error handling and validation
* Improving the search functionality
* Using PostgreSQL for a production deployment
* Implementing a real payment gateway integration
* Improving security and production configuration
* Adding a REST API
* Further improving the project architecture

## Project Status

Universe-Game is maintained as a **portfolio and educational project**.

The repository represents the project developed for my bachelor's final project, with selected improvements to make it more suitable for public presentation.

It is intended to demonstrate my practical experience with **Python, Django, databases, authentication, and backend web development** rather than to represent a production-ready commercial platform.
