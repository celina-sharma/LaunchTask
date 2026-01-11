# Week 5 – Day 2  
## Multi-Container Application using Docker Compose

---

## Objective

The objective of this task is to deploy and manage a **multi-container application** using **Docker Compose**, ensuring:

- Proper container-to-container networking
- Persistent storage using Docker volumes
- Verified communication between client and server
- One-command lifecycle management of services

---

## Application Architecture

The application consists of **three services** running as separate containers:

### 1. Client (Frontend)
- Runs as a static frontend application
- Exposed on **port 3000**
- Communicates with the backend server using HTTP requests

### 2. Server (Backend)
- Built using **Node.js and Express**
- Exposed on **port 5000**
- Handles API requests from the client
- Connects to MongoDB using Mongoose

### 3. MongoDB (Database)
- Uses the official MongoDB Docker image
- Runs internally on **port 27017**
- Stores data in a Docker volume for persistence

---

## Docker Compose Configuration

All services are defined in a single `docker-compose.yml` file.  
Docker Compose is used to manage the entire application stack.

### Start all services after doing changes
```bash
docker compose up -d
docker compose up -d --build
docker exec -it ['container name'] /bin/sh -> to start new terminal in a container after doing changes.