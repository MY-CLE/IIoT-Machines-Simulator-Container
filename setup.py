import os

os.chdir("frontend")
os.system("npm install")
os.system("npx tailwindcss -i ./input.css -o ./src/css/output.css")
os.system("npm run build")
