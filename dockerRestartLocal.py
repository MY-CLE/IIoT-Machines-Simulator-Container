import os

os.chdir("frontend")
os.system("tsc")
os.chdir("..")
os.system("python ./setup.py")
os.system("docker compose down")
os.system("docker rmi flask-api:local nginx-service:local")
os.system("docker compose up")
