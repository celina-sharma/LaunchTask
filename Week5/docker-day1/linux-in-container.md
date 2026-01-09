# Linux Inside Docker Container

## Objective
To understand how Linux OS operations work inside a running Docker container and how containers behave differently from virtual machines.

---

## Container Access
The running container was accessed using:

docker exec -it week5-node-container /bin/sh

This provides shell access similar to SSH into a server.

---

## File System Exploration
Commands used:
- pwd
- ls
- ls /

Observations:
- The working directory inside the container is `/app`
- The container has an isolated and minimal Linux filesystem
- Only required directories and application files are present

---

## Process Management
Commands used:
- ps
- ps aux

Observations:
- Very few processes are running inside the container
- The Node.js application (`node index.js`) runs as PID 1
- If PID 1 stops, the container exits automatically

---

## Resource Monitoring
Command used:
- top

Observations:
- CPU and memory usage are minimal
- Resources are isolated using Linux cgroups

---

## Disk Usage
Commands used:
- df -h
- du -sh /app

Observations:
- The container uses a lightweight filesystem
- Application files consume very little disk space

---

## Logs
Logs were viewed using:

docker logs week5-node-container

Observations:
- Logs are written to STDOUT by the Node.js application
- Docker captures logs from the main process (PID 1)
- No log files are maintained inside the container

---

## Conclusion
Docker containers provide isolated, lightweight Linux environments that share the host kernel. They are efficient, fast to start, and suitable for running production server-side applications.
