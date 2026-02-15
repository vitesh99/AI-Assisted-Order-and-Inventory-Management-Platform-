AI-Assisted Order & Inventory Management Platform

Production-Grade Microservices System | FastAPI | PostgreSQL | Docker | React | OpenRouter

Overview

This project demonstrates the evolution of a modular backend into a distributed microservices architecture with an AI-assistive layer designed for resilience and scalability.

The system consists of independently deployable services for Authentication, Inventory Management, and Order Processing, orchestrated through an API Gateway. AI capabilities are integrated as a non-blocking enhancement layer to preserve core system reliability.

The design emphasizes:

Service isolation

Stateless authentication

Fault tolerance

Graceful degradation

Production-ready containerization

High-Level Architecture
Service	Internal Port	Exposed Port	Responsibility
API Gateway	8000	8000	Routing, request aggregation, entry point
Auth Service	8001	—	User management, JWT issuance
Inventory	8002	—	Product catalog & stock management
Orders	8003	—	Order lifecycle & AI integration
Frontend	3000	3000	React (Vite) UI
PostgreSQL	5432	5432	Persistent storage (isolated schemas)

All backend services are containerized and orchestrated using Docker Compose.

Architectural Decisions
1. Microservices Decomposition

The system was refactored from a modular monolith into independently deployable services based on clear domain boundaries:

Auth → Identity & security

Inventory → Product & stock domain

Orders → Transactional order processing

This enables:

Independent scalability

Fault isolation

Parallel development

Clear domain ownership

2. Stateless Authentication

JWT tokens issued by Auth service

Claims embedded within tokens

Services validate tokens locally (no synchronous call to Auth)

This removes authentication as a runtime dependency and improves availability.

3. Data Isolation Strategy

PostgreSQL as persistent store

Logical separation via independent schemas/databases

No cross-service table access

All inter-service communication occurs via HTTP APIs

This enforces service boundaries and prevents tight coupling.

AI Assistive Layer

AI is integrated inside the Order Service as a non-blocking enhancement.

Design Goals

AI must never impact order creation latency

AI failures must not break business flows

AI must degrade gracefully

Implementation Strategy

Background task execution for AI calls

Timeout handling

Exception isolation

Retry logic

Circuit-breaker-like safeguards

If OpenRouter is unavailable:

Order creation succeeds

AI summary remains empty

System continues operating normally

AI is treated as an augmentation layer — not a critical dependency.

Failure Handling & Resilience

Gateway returns appropriate HTTP status codes (503 on downstream failure)

Inventory client handles connection errors explicitly

Services log failures without crashing

Stateless JWT reduces runtime dependency chains

Inter-service calls wrapped with structured error handling

Production Considerations Implemented

Dockerized services

Isolated containers per domain

Environment-based configuration

Structured logging

Async request handling (FastAPI)

Input validation via Pydantic models

Clear separation of concerns (routes / services / schemas)

Trade-offs Considered
Concern	Monolith	Microservices
Deployment	Simple	More complex
Scalability	Coarse	Fine-grained
Latency	Low	Slightly higher
Complexity	Lower	Higher

Microservices were chosen to demonstrate distributed system design patterns relevant to production environments.

Tech Stack

Backend:

Python

FastAPI

AsyncIO

PostgreSQL

JWT Authentication

Docker / Docker Compose

Frontend:

React (Vite)

Axios

Minimal, clean UI for operational clarity

AI Layer:

OpenRouter API

Async background execution

Graceful degradation strategy

How to Run
Backend
docker-compose up --build


Services will be available at:

Gateway → http://localhost:8000

API Docs → http://localhost:8000/docs

Frontend
cd frontend
npm install
npm run dev


Frontend runs at:

http://localhost:3000


![alt text](<Screenshot 2026-02-15 120423.png>)
![alt text](<Screenshot 2026-02-15 120439.png>)
![alt text](<Screenshot 2026-02-15 120514.png>)