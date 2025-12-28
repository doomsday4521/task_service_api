# Task Service API

A production-style asynchronous backend API built with FastAPI, featuring secure JWT authentication with refresh token rotation and user-scoped task management.

This project demonstrates real-world backend patterns: authentication lifecycle management, ownership-safe CRUD, layered architecture, and PostgreSQL persistence.

---

## Tech Stack

- **FastAPI** – async Python web framework  
- **PostgreSQL** – relational database  
- **SQLAlchemy (async)** – ORM  
- **Alembic** – database migrations  
- **JWT** – access tokens  
- **Refresh Tokens** – rotation + revocation  
- **Python 3.11+**

---

## Core Features

### Authentication
- User registration and login
- Short-lived **access tokens**
- Long-lived **refresh tokens** stored hashed in DB
- Refresh token **rotation**
- Secure **logout** via refresh token revocation
- Protected routes using dependency-based auth

### Task Management
- Create, read, update, delete tasks
- Tasks are strictly **user-owned**
- Ownership enforced at DB query level
- Pagination and ordering
- Partial updates (PATCH)

### Architecture
- Clear separation of concerns:
  - **Routes** → HTTP layer
  - **Services** → business logic
  - **Repositories** → database access
- Async DB access throughout
- No trust in client-provided user identifiers

---

## Authentication Flow

