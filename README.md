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

## Start the Application

To start the updated docker images please use the start.sh script found in the root of the project.

```
bash start.sh
```

Now you should be able to access localhost and see a almost default react app, the time displayed is provided by the flask backend
