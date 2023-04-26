#!/bin/bash
docker compose kill
docker build -f backend/Dockerfile -t flask-api .
docker build -f nginx/Dockerfile -t nginx-service .
docker compose up -d --remove-orphans