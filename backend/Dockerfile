FROM python:3.10.11-alpine3.17

# https to http
RUN sed -ie "s/https/http/g" /etc/apk/repositories

# check for updates & install sqlite3 db
RUN apk update && apk upgrade
RUN apk add --no-cache sqlite

# http to http
RUN sed -ie "s/http/https/g" /etc/apk/repositories

WORKDIR /home/iiot-machine-sim/database

# Copy create_tables.sql to container
COPY backend/database/create_tables.sql .

# Create database
RUN sqlite3 machine-sim.db

# Execute create_tables.sql on the machine-sim.db database
RUN sqlite3 machine-sim.db < create_tables.sql


WORKDIR /home/iiot-machine-sim/

COPY backend/requirements.txt backend/ ./
RUN pip install --trusted-host pypi.org -r ./requirements.txt

CMD sqlite3 machine-sim.db & python3 -m flask run --host=0.0.0.0