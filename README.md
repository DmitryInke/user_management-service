
# User Management Service

This is a FastAPI-based User Management Service that includes features such as user registration, login, token-based authentication, and user profile management. The service uses PostgreSQL as the database and Redis for caching and token revocation.

## Features Implemented

 - **User Registration**: Register new users with first name, last name, email, and password.
 - **User Login**: Authenticate users and generate JWT access tokens.
 - **Token Revocation**: Use Redis to store and validate short-lived access tokens.
 - **User Profile Management**: Retrieve and update user profile details.
 - **Caching**: Cache user profiles using Redis for better performance.

## How to Run the Project

### Prerequisites
- Python 3.10+
- Docker

### Running the Project Locally
1. Create a `.env` File:
   ```env
   SQLALCHEMY_DATABASE_URL=postgresql://user:example@localhost:5432/user_db
   JWT_SECRET=c8SjrTFisjT7CkJ2SunYHiE6PPe1E6ah
   JWT_EXPIRATION=15
   REDIS_HOST=localhost
   REDIS_PORT=6379
   ```
2. Install Dependencies
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run database and redis services using Docker Compose:
   ```bash
   docker-compose up db redis --build
   ```
4. Run the app
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Running the Project with Docker
1. Create a `.env` File:
   ```env
   SQLALCHEMY_DATABASE_URL=postgresql://user:example@db:5432/user_db
   JWT_SECRET=c8SjrTFisjT7CkJ2SunYHiE6PPe1E6ah
   JWT_EXPIRATION=15
   REDIS_HOST=redis
   REDIS_PORT=6379
   ```
2. Run Docker Compose
   ```bash
   docker-compose up --build
   ```

## Notes
- There will be a file `Users Management System.postman_collection.json` in the root folder for Postman to use all the endpoints.

