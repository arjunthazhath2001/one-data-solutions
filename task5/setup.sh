#!/bin/bash

echo "Preparing environment..."
docker-compose down

echo "Building Docker images..."
docker-compose build

echo "Starting up containers..."
docker-compose up -d

echo "Waiting 5 seconds for containers to stabilize..."
sleep 5

echo "Current container status:"
docker-compose ps

echo "All services are up and running!"

echo "Tailing logs (Press Ctrl+C to exit)..."
docker-compose logs -f
