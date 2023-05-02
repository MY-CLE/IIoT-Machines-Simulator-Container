#!/bin/bash
docker-compose kill
docker build --no-cache -f backend/Dockerfile -t flask-api .
docker build --no-cache -f nginx/Dockerfile -t nginx-service .
docker build --no-cache -f database/Dockerfile -t database .
docker-compose up -d --remove-orphans