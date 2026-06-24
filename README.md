# (BeyondCRUD)

A professional book inventory management backend built using **FastAPI**, **SQLModel** (SQLAlchemy + Pydantic), and **PostgreSQL**. The project features secure JWT-based authentication, password hashing, database migrations via Alembic, and Token Blacklisting using Redis.

## Features

- **Book Inventory Management**: Complete CRUD operations for managing books.
- **User Authentication**: Secure signup and login endpoints using JWT access and refresh tokens.
- **Security & Authorization**: Password hashing (Bcrypt) and endpoint protection.
- **Database Migrations**: Managed via Alembic.
- **Token Blacklisting**: Revocation of blacklogged/logged-out JWT tokens via Redis.

---

## Tech Stack

- **Framework**: FastAPI (Asynchronous Python Web Framework)
- **Database**: PostgreSQL (Neon Serverless/Local Postgres)
- **ORM / Database Tools**: SQLModel, SQLAlchemy, Alembic (Migrations)
- **Caching / Key-Value Store**: Redis
- **Security**: JWT (PyJWT), Passlib (Bcrypt)

---

## Getting Started

### 1. Prerequisites

Ensure you have the following installed on your local machine:
- Python 3.10+
- PostgreSQL
- Redis Server (local or cloud instance)

### 2. Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd BeyondCRUD
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:
   - **Windows (PowerShell)**:
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**:
   Copy the example environment file and configure your credentials:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your database URL, JWT secret key, and Redis configuration.

---

## Database Migrations

This project uses **Alembic** for managing database schema changes.

- **Apply Migrations (Upgrade database to latest schema)**:
  ```bash
  alembic upgrade head
  ```

- **Create a New Migration**:
  ```bash
  alembic revision --autogenerate -m "description of changes"
  ```

---

## Running the Application

Start the local development server using Uvicorn:

```bash
uvicorn BeyondCRUD:app --reload
```

Once running, you can access:
- **API Documentation (Swagger UI)**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative Documentation (ReDoc)**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
