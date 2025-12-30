# Architecture – Week 4 Day 1

## Overview
This backend implements a production-oriented Node.js architecture focusing on controlled startup, environment-driven configuration, dependency orchestration, centralized logging, and graceful shutdown.

---

## Startup & Lifecycle
The application follows a deterministic startup sequence:
1. Load environment-specific configuration
2. Initialize logger
3. Connect to the database
4. Create and configure the Express app
5. Start the HTTP server
6. Register shutdown handlers

The server starts only when all critical dependencies are ready.

---

## Configuration
A centralized config loader dynamically loads `.env.local`, `.env.dev`, or `.env.prod` based on `NODE_ENV`. Configuration is exposed through a single config object, avoiding direct use of `process.env`.

---

## Loaders
Loaders are used to initialize startup dependencies:
- **Database Loader**: Manages MongoDB connection and fails fast if unavailable
- **Application Loader**: Creates and configures the Express app without starting the server

---

## Logging
A centralized logger replaces `console.log` and provides structured logs for startup, errors, and system events.

---

## Shutdown Handling
The application listens for process termination signals and performs a clean shutdown by stopping new requests and closing the server before exiting.

---

## Scope
This document covers **Week-4 Day-1**, focused on backend bootstrapping and lifecycle management.
