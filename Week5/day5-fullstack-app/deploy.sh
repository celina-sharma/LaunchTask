#!/bin/bash

echo "Starting Production Deployment with HTTPS"

if [ ! -f .env ]; then
    echo "Error: .env file missing! Create it with MONGO credentials."
    exit 1
fi

if [ ! -f ./nginx/certs/localhost.pem ]; then
    echo " Error: SSL certificates not found in ./nginx/certs/"
    echo "Please run: mkcert -key-file nginx/certs/localhost-key.pem -cert-file nginx/certs/localhost.pem localhost 127.0.0.1 ::1"
    exit 1
fi

echo "Stopping old containers..."
docker compose -f docker-compose.prod.yml down --remove-orphans

echo "Building and starting services..."
docker compose -f docker-compose.prod.yml up -d --build

echo "Cleaning up unused Docker images..."
docker image prune -f

echo "Deployment Successful!"
echo "Access your secure app at: https://localhost"