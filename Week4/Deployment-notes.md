# Deployment Notes – Week 4 Backend System

# 1. Overview
This project is a production-ready Node.js backend application designed with:
- Environment-driven configuration
- Controlled startup & graceful shutdown
- Background job processing using queues
- API and worker process separation
- Structured logging and request tracing
- Secure middleware stack
- PM2-based process management

---

## 2. Tech Stack
- **Runtime:** Node.js (ES Modules)
- **Framework:** Express.js
- **Database:** MongoDB
- **Queue & Jobs:** BullMQ
- **Cache/Broker:** Redis
- **Process Manager:** PM2
- **Logging:** Pino
- **Validation:** Zod
- **Security:** Helmet, CORS, Rate Limiting

---
## 3. Startup and lifecycle management
- Application startup is controlled via a bootstrap sequence:
  - Load configuration
  - Connect to database
  - Register middleware
  - Mount routes
  - Start server
- Graceful shutdown is handled using process signals (SIGINT).


## 4. Background Job Architecture
- API enqueues background jobs using BullMQ
- Redis acts as the queue broker
- Email worker runs as a separate process
- Retry mechanism with exponential backoff is enabled
- API response is non-blocking (`202 Accepted`)

This ensures long-running tasks do not block HTTP requests.

---

## 5. Logging & Observability
- Logging is implemented using **Pino**
- Logs are written to:
  - Console (development)
  - `logs/app.log` (file-based logging)
- Each request and background job includes a unique `requestId`
- Logs are structured to allow filtering and tracing across processes

Example log fields:
level, timestamp, pid, requestId, message


---

## 8. Security Measures
The backend includes multiple security layers:
- Helmet for HTTP security headers
- CORS policy enforcement
- Rate limiting to prevent abuse
- Payload size limits to prevent large-body attacks
- Input validation using Zod schemas
- Centralized error handling with consistent error responses

---

## 9. PM2 Process Management

### PM2 Responsibilities
- Runs API and worker as separate processes
- Handles restarts on failure
- Supports production and development modes
- Maintains process isolation

### Start with PM2
```bash
pm2 start src/prod/ecosystem.config.cjs