FROM python:3.10.11-alpine3.17

RUN apk update && apk upgrade
RUN apk add --no-cache sqlite

WORKDIR /home/sqlite

# Copy create_tables.sql to container
COPY backend/database/create_tables.sql .

# Create database
RUN sqlite3 machine-sim.db

# Execute create_tables.sql on the machine-sim.db database
RUN sqlite3 machine-sim.db < create_tables.sql

# Enter Container with SQLite3 CLI
FROM python:3.10-alpine

COPY backend/requirements.txt backend/app.py backend/.flaskenv ./
RUN pip install -r ./requirements.txt
ENV FLASK_ENV production

CMD sqlite3 machine-sim.db & python3 -m flask run --host=0.0.0.0