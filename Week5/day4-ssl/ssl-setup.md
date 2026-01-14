# SSL Setup using NGINX and mkcert (Day 4)
 
This document describes how HTTPS was implemented using NGINX inside Docker with self-signed certificates generated via mkcert. SSL/TLS is terminated at NGINX, while backend services communicate over HTTP inside a secure Docker network.
 
## Architecture
 
Browser → HTTPS → NGINX (SSL Termination) → HTTP → Backend-1 / Backend-2
 
This approach centralizes security, simplifies backend services, and follows real-world production architecture.
 
## Why HTTPS
HTTP traffic is unencrypted and can be intercepted or modified. HTTPS encrypts data, ensures integrity, and verifies server identity using certificates. Modern browsers require HTTPS for secure communication.
 
## Why SSL Termination at NGINX
NGINX handles encryption and decryption so backend services remain simple HTTP servers. This improves performance, reduces complexity, and allows centralized certificate management.
 
## Tools Used
NGINX for reverse proxy and SSL termination, mkcert for generating locally trusted certificates, Docker and Docker Compose for container orchestration.
 
## mkcert
sudo apt install -y libnss3-tools mkcert ------ installs mkcert and browser trust dependencies
mkcert -install--------------------------------- creates and installs  local certificate authority (trusted)
mkcert myapp.local------------------------------ generates SSL certificates for the local domain myapp.local
 
 
 