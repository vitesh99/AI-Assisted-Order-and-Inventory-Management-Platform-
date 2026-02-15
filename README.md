# AI-Assisted Order and Inventory Management Platform

**Production-Grade Microservices Architecture**

This project demonstrates the evolution of a modular monolith into a scalable microservices system. It features separate services for Authentication, Inventory, and Order Management, orchestrated by a Gateway and powered by an AI assistive layer.

## Architecture Overview

| Service | Port (Internal) | Port (Exposed) | Responsibility |
| :--- | :--- | :--- | :--- |
| **Gateway** | 8000 | 8000 | API Proxy, Routing, Aggregation |
| **Auth** | 8001 | - | User Management, JWT Issuance |
| **Inventory** | 8002 | - | Product Catalog, Stock Management |
| **Orders** | 8003 | - | Order Processing, AI Integration |
| **Frontend** | 3000 | 3000 | React UI (Vite) |
| **PostgreSQL**| 5432 | 5432 | Shared DB Instance (Separate Schemas/DBs) |

---

## 1. Why Microservices?

We migrated from a modular monolith to microservices to achieve:
-   **Independent Scalability**: Examples: Scaling the `order-service` during Black Friday without duplicating `inventory-service`.
-   **Fault Isolation**: If the `ai-module` in `order-service` crashes or hangs, it does not affect `login` (Auth) or `product-browsing` (Inventory).
-   **Technology Agnosticism**: Each service can technically use a different stack (though we stuck to FastAPI/Python for consistency).
-   **Team Autonomy**: Different teams can own different services.

## 2. Trade-offs (Monolith vs Microservices)

| Feature | Modular Monolith | Microservices (Current) |
| :--- | :--- | :--- |
| **Complexity** | Low (Single codebase) | High (Distributed system, net calls) |
| **Deployment** | Simple (One Docker container) | Complex (Orchestration required) |
| **Consistency** | ACID Transactions (easy) | Eventual Consistency (harder) |
| **Latency** | Function calls (nanoseconds) | HTTP/RPC calls (milliseconds) |

**We chose Microservices here/now to demonstrate advanced architectural patterns (Gateway, Stateless Auth, Inter-service communication).**

## 3. Storage Strategy

-   **Database**: PostgreSQL is used.
-   **Isolation**: Each service connects to its own logical database (`ai_inventory_auth`, `ai_inventory_orders`, etc.).
-   **No Shared State**: Services do NOT read each other's tables. They communicate via HTTP APIs.

## 4. AI Isolation Strategy

The AI Layer is embedded within the **Order Service** but runs as a **Background Task**.
-   **Non-Blocking**: Order creation returns immediately. AI runs asynchronously.
-   **Resilient**: If OpenRouter/Gemini is down, the order is still created. The summary field just remains empty (Graceful Degradation).
-   **Circuit Breaker**: We use timeouts and try/catch blocks to ensure AI failures don't crash the service.

## 5. Failure Handling

-   **Gateway**: Handles routing failures (503 Service Unavailable).
-   **Inter-Service**: `InventoryClient` in `order-service` handles connection errors to Inventory.
-   **Auth**: Stateless JWTs mean `order-service` validates tokens without hitting `auth-service` for every request (High Availability).

## 6. SDE Interview Explanation

*"I took a modular monolith and decomposed it into microservices. I established domain boundaries (Auth, Inventory, Orders) and decoupled the database. I implemented a Gateway pattern to simplify the frontend client. I solved the distributed authentication problem using stateless JWTs with embedded claims. For the AI feature, I used background tasks to ensure the core checkout flow remains fast and reliable, treating AI as an enhancement rather than a critical dependency."*

---

## How to Run

See [SETUP_GUIDE.md](.gemini/antigravity/brain/9ffb0640-3ca5-43e0-8f6d-9b3208db0022/setup_guide.md) (Checking Artifacts) for detailed instructions.

**Quick Start:**
1.  **Backend**: `docker-compose up --build`
2.  **Frontend**: `cd frontend && npm install && npm run dev`
