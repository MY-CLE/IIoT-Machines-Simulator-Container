# IIoT-Machines-Simulator-Container
# Contents
1. [Onboarding](#onboarding)
2. [Development Flow](#development-flow)
3. [Depolyment](#deployment)
4. [Project Links](#links)

# Onboarding

## Backend
To ensure that all dependencies have the right version, we use a virtual environment.
Install the virtualenv:
```
pip install --user virtualenv 
```
after we installed sucessfully installed virtualenv we need to initialize a venv in the backend folder
```
cd backend
python3 -m venv venv
```
Now that we have initialized the venv we now need to activate it. This command depends on your operating system. Please make sure your terminal is in /backend
**Linux/MacOs:**
```
source venv/bin/activate
```
**Windows:**
```
.\venv\Script\activate
```
When venv is active we can install all dependencies using the requirements.txt
```
pip install -r requirements.txt
```

## Frontend
To install all necessary dependencies you can use the setup.py or run the commands yourself. Make sure that you are in the root folder of the project:
```
python3 setup.py
```
or
```
cd frontend
npm install
npx tailwindcss -i ./input.css -o ./src/css/output.css
npm run build
```
# Development Flow
## Backend
The development flow for backend develpment is pretty simple. We just need to start up the virtual environment again.
**Linux/MacOs:**
```
source venv/bin/activate
```
**Windows:**
```
.\venv\Scripts\activate
```
To start the flask application we need to run 
```
flask run
```

## Fronted
To start the development process for fronted we need to start some running process.

### Start React app
Depending on the starting environment we need to run different start scripts

#### Development with local flask app
If you are developing with a local version of the flask api running we use the start script start:local

```
npm run start:local
```

#### Development with Postman mock server
If you are developing with postman mock server we use the start script start:mock, in this case we don't need to start the local flask api.

```
npm run start:mock
```

### Start tailwind watch
In order to update the tailwind output.css while developing you need to start the following command in a new terminal in the frontend folder
```
npx tailwindcss -i ./input.css -o ./src/css/output.css --watch
```

### Start the typescript watch
When developing in vs code, you can start a typescript watch service by pressing ctrl + shift + b and selecting the typescript watch option. 

# Deployment
To create a compact application,  we use docker compose. We have 3 separate docker-compose.yml files to compile for 2 different platforms
## Build frontend
We need to create a new build version of our frontend. In order to do that we run setup.py
```python3 setup.py``` 
## Docker build
After creating an up-todate build files from the react app, we use docker compose to build the 2 images.
We build docker images for 2 different platforms, for amd64 and arm/v7  

If you are on a **linux environment** make sure that you have `docker-buildx` installed. You can install it via your distibutions paketmanager.

### amd64
```
docker buildx build --platform linux/amd64 -t adstec/priv:flask-api-amd64 -f "backend/Dockerfile" .
docker buildx build --platform linux/amd64 -t adstec/priv:nginx-service-amd64 -f "nginx/Dockerfile" .
```
### arm/v7
```
docker buildx build --platform linux/arm/v7 -t adstec/priv:flask-api-arm-v7 -f "backend/Dockerfile" .
docker buildx build --platform linux/arm/v7 -t adstec/priv:nginx-service-arm-v7 -f "nginx/Dockerfile" .
```


## Docker compose
To start the docker application, we use docker compose. We have 3 seperate docker compose files to compose for the 2 platforms

### local development
```
docker compose -f "docker-compose.yml" up
```
### amd64
```
docker compose -f "docker-compose-amd64.yml" up
```
### arm/v7
```
docker compose -f "docker-compose-armv7.yml" up
```
## Deleting old files
To delete outdated docker images, all depending docker container have to be deleted first.

### Removing Container
We can achive this by either removing them by hand with `docker rm [IMAGE NAME]` or use docker compose down:
```
docker compose down
```
or
#### amd64
```
docker rm flask-api-amd64
docker rm nginx-service-amd64
```
#### arm/v7
```
docker rm adstec/priv:flask-api-arm-v7
docker rm adstec/priv:nginx-service-arm-v7
```

### Removing Images

Now we can remove the images
#### amd64
```
docker rmi adstec/priv:flask-api-amd64
docker rmi adstec/priv:nginx-service-amd64
```

#### arm/v7
```
docker rmi adstec/priv:flask-api-arm-v7
docker rmi adstec/priv:nginx-service-arm-v7
```

## Using Dockerhub
In order to share the created Docker images we can use docker hub. We can use ```docker pull``` and  ```docker push``` .

### Docker login
You need to first login to docker. Use the provided project email and password
```
docker login 
```
### Docker push
The docker push command depends on the platform you build the images for:

#### amd64
```
docker push adstec/priv:nginx-service-amd64
docker push adstec/priv:flask-api-amd64
```
#### arm/v7
```
docker push adstec/priv:nginx-service-arm-v7
docker push adstec/priv:flask-api-arm-v7
```

### Docker pull
Please make sure you are logged in order to pull a docker container.

#### amd64
```
docker pull adstec/priv:nginx-service-amd64
docker pull adstec/priv:flask-api-amd64
```
#### arm/v7
```
docker pull adstec/priv:nginx-service-arm-v7
docker pull adstec/priv:flask-api-arm-v7
```
# Contact
If you have problems or questions while using this project please send an email to myclesmwtproject@gmail.com or open a issue in this repository.

## Links
Here is a link to the complete [dokumentation](https://1drv.ms/w/s!ArSpht_ylea5gtojCA0xuxnLwjGezA?e=OemQSR) of this project.

We held a [presentation](https://1drv.ms/p/s!ArSpht_ylea5gtoniz53YU4JZscPyg?e=0rGWFA) about the progress of this project.

To have a look at our UI mock up please head to this [figma project](https://www.figma.com/file/F5FVOZLBPZQf3Kl5RMDlkJ/HMI-Prototyp?node-id=0%3A1&t=7RfpV0oQdLpqFMub-1).

To view our simulator api please click [here](https://documenter.getpostman.com/view/24866334/2s93ebRVN2).
