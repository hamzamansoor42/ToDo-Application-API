# Task Management Application

A simple Flask-based web application for user management and task management functionalities with JWT authentication.

## Features

- User registration and login with JWT authentication
- CRUD operations for tasks (Create, Read, Update, Delete)

## Project Structure
    /todo-application-api
        /controllers
            users.py
            tasks.py
        /models
            models.py
        /utils
            config.py
            db.py
        /migrations
        manage.py
        app.py
        Dockerfile
        docker-compose.yml
        .env
        requirements.txt
        README.md



## Project Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.11 or higher (for local development outside Docker)
- PostgreSQL database

### Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/hamzamansoor42/ToDo-Application-API.git
   cd ToDo-Application-API

2. **Create .env file:**
    Create a .env file in the root directory of the project with the following content:
    ```bash
    DATABASE_URL=postgresql://username:password@db:5432/yourdbname
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    POSTGRES_USER=username
    POSTGRES_PASSWORD=password
    POSTGRES_DB=database_name

3. **Build the Containers:**
    ```bash
    docker-compose build

4. **Initialize the Database:**
    Run the following commands to set up the database schema:
    ```bash
    docker-compose run web flask db init
    docker-compose run web flask db migrate -m "Initial migration"
    docker-compose run web flask db upgrade

5. **Running the Application:**
    The Flask application will be available at http://localhost:5000. You can access it using your browser or API clients like Postman.
    ```bash
    docker-compose up

6. **Running tests:**
    To run the tests using Docker, execute:
    ```bash
    docker-compose run tests

### Endpoints
Here’s a summary of the API endpoints:

- POST /register: {"username": "testuser", "password": "testpassword"}
- POST /login: {"username": "testuser", "password": "testpassword"}
- GET /tasks: Requires authentication
- POST /tasks: {"task": "New task"} (Requires authentication)
- PUT /tasks/{task_id}: {"task": "Updated task"} (Requires authentication)
- DELETE /tasks/{task_id}: Requires authentication
- GET /tasks/{task_id}: Requires authentication