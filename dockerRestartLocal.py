import os

os.system("docker compose down")
os.system("docker rmi flask-api:local nginx-service:local")
os.system("docker compose up")
