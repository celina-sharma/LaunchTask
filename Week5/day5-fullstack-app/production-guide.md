### Production Deployment & SSL Setup (Day 5)

### Architecture
All traffic enters through a secure NGINX gateway before being routed to the internal application services.
Browser (HTTPS) → NGINX (SSL Termination) → Backend (Node.js) → Database (MongoDB)

### Security & SSL Implementation
HTTPS ensures that all data sent between the browser and our server is encrypted. For a "Message Board," this protects user privacy and prevents attackers from sniffing traffic.
By handling SSL at NGINX, our Backend remains lightweight and focused only on application logic. NGINX is optimized for high-performance encryption/decryption.

Tools Used
NGINX: Reverse proxy and SSL termination.
mkcert: Generates locally trusted SSL certificates.
Docker Hub: Centralized registry hosting our production images.


# Setup & Deployment
1. SSL Certificate Generation
We use mkcert to create certificates that our local browser will trust without warnings.

Bash

# Create directory for certificates
mkdir -p nginx/certs

# Generate certificates for localhost
mkcert -key-file nginx/certs/localhost-key.pem -cert-file nginx/certs/localhost.pem localhost 127.0.0.1 ::1

# Automated Deployment
Instead of manual commands, we use a deploy.sh script to ensure a clean, repeatable environment.
chmod +x deploy.sh
./deploy.sh


# Reliability Features (Production-Ready)
Healthchecks: NGINX will not route traffic until the Backend is (healthy), and the Backend will not start until the Database is (healthy).
Containers use restart: always to automatically recover from system reboots or process crashes.
Log Management: Container logs are capped at 10MB using the json-file to prevent the server from running out of disk space.
Persistence: Data is saved in a named Docker volume (mongo_data), ensuring messages survive container restarts or updates.

# Accessing the Application
Secure Frontend: https://localhost
API Health Check: https://localhost/api/health