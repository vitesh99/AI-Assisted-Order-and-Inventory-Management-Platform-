<<<<<<< HEAD
# AI-Assisted-Order-and-Inventory-Management-Platform-
=======
# AI Assisted Order and Inventory Management Platform (Phase 1)

This is a production-lean FastAPI backend for an Order and Inventory Management Platform.

## Features

- **Authentication**: JWT-based signup and login.
- **Inventory Management**: Add items, update quantities, list items.
- **Order Management**: Create orders with stock validation, list user orders.
- **Clean Architecture**: Modular monolith with separation of concerns.

## Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: SQLite (via SQLAlchemy)
- **Authentication**: OAuth2 with Password (Bearer with JWT)
- **Containerization**: Docker & Docker Compose

## Project Structure

```
app/
  core/         # Config, Security, Database
  models/       # SQLAlchemy Models
  schemas/      # Pydantic Schemas
  api/          # API Routes & Dependencies
  main.py       # Entry Point
```

## How to Run

### Using Docker (Recommended)

1.  Build and run the container:
    ```bash
    docker-compose up --build
    ```
2.  Access the API documentation at:
    -   Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
    -   ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Local Development

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn app.main:app --reload
    ```

## API Usage Flow

1.  **Signup**: `POST /api/v1/auth/signup`
2.  **Login**: `POST /api/v1/auth/login` (Copy the `access_token`)
3.  **Authorize**: Click "Authorize" in Swagger UI and paste the token.
4.  **Manage Inventory**: `POST /api/v1/inventory/` (Requires Auth)
5.  **Create Order**: `POST /api/v1/orders/` (Requires Auth, items must exist in inventory)

## Design Decisions

-   **SQLite**: Chosen for simplicity and ease of setup in restricted environments. Can be easily swapped for PostgreSQL.
-   **Sync vs Async**: Used synchronous SQLAlchemy for simplicity and stability in Phase 1.
-   **Modular Monolith**: structured for scalability without the operational complexity of microservices.

## Limitations (Phase 1)

-   No real payment processing.
-   No email notifications.
-   Basic stock locking (no strict row-level locking for high concurrency).
-   SQLite is not suitable for high-write production loads.
>>>>>>> 387b2ff (Phase 1: Core FastAPI order and inventory platform)



