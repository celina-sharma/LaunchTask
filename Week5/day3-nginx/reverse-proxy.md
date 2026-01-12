# Week 5 – Day 3  
## NGINX Reverse Proxy & Load Balancing using Docker Compose

---
## Objective

The objective of this task is to implement **NGINX as a reverse proxy** and demonstrate **round-robin load balancing** between multiple backend services using **Docker Compose**.

This task ensures:
- Reverse proxy configuration using NGINX
- Multiple backend instances
- Traffic distribution using load balancing
- Container-to-container networking
- Verification using `curl`

---

## Architecture

- NGINX acts as a **single entry point** for client requests
- Two backend containers run **identical Node.js services**
- Backend services are hidden from the client
- All services run inside Docker containers

---

## Request Flow

1. Client sends a request to the NGINX endpoint
2. NGINX receives the request on the exposed port
3. NGINX forwards the request to one of the backend containers
4. Backend processes the request and sends the response back via NGINX

---

## Routing

- Client requests are made to the `/api` endpoint
- NGINX routes `/api` requests to backend services
- Clients never directly access backend containers

---

## Load Balancing

- NGINX uses **round-robin load balancing** by default
- Each incoming request is forwarded to a different backend instance
- Load balancing is verified by observing different backend responses for repeated requests

---

## Networking

- Docker Compose creates a shared internal network
- Backend services are accessed using **service names** instead of IP addresses
- NGINX resolves backend services using Docker’s internal DNS

## Request Flow

Client (curl / browser)
|
v
NGINX (port 8080)
|
|-- Backend 1 (Node.js, port 3000)
|
|-- Backend 2 (Node.js, port 3000)


---

## Key Learnings

- NGINX acts as a reverse proxy to hide internal services
- Load balancing distributes traffic evenly across backend instances
- Docker Compose simplifies multi-container orchestration
- Using a single entry point improves scalability and maintainability
- NGINX is widely used in real-world production environments

---

## Conclusion

This setup successfully demonstrates **NGINX-based reverse proxying and load balancing** using Docker.  
The architecture provides improved scalability, clean separation of services, and a production-ready traffic handling approach.
