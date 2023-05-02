FROM keinos/sqlite3

WORKDIR /home/sqlite

# Copy create_tables.sql to container
COPY database/create_tables.sql .

# Create database
RUN sqlite3 machine-sim.db

# Execute create_tables.sql on the machine-sim.db database
RUN sqlite3 machine-sim.db < create_tables.sql

# Enter Container with SQLite3 CLI
CMD ["sqlite3", "machine-sim.db"]

