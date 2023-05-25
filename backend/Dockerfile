FROM python:3.9.16-alpine3.17

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

# Copy backend files to container
COPY backend/ ./

# Install requirements
RUN pip install --upgrade pip
RUN pip install https://www.piwheels.org/simple/lxml/lxml-4.9.2-cp39-cp39-linux_armv7l.whl#sha256=7311648ee07bbc399f64f3605de71b0f8def24bb90eb68796cfabd2ed4f2c9f3
RUN pip install -r ./requirements.txt

CMD sqlite3 machine-sim.db & python3 -m flask run --host=0.0.0.0