# IIoT-Machines-Simulator-Container

# Getting started

1. Create a virtual enviornment in /backend
   using

```
cd backend
python3 -m venv venv
```

2. activate the environment using

```
source venv/bin/activate
```

3. run pip install

```
pip install -r requirements.txt
```

4. cd into frontend and run

```
cd ../frontend
npm install
npm run build
```

## Docker Compose

the following commands have to be executed in the right folder

1. flask image

```
cd backend
docker build -f Dockerfile.backend -t flask-api .

```

2. react app

```
cd frontend
docker build -f Dockerfile.frontend -t react-app .
```

3. nginx image

root folder

```
cd ..
sudo docker build -f nginx/Dockerfile.nginx -t nginx-service .
```

4. docker compose
   root folder

```
docker-compose up
```

Now you should be able to access localhost and see a almost default react app, the time displayed is provided by the flask backend
