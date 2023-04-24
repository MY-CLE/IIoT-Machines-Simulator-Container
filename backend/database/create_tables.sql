CREATE TABLE snapshots (
	snapid INTEGER PRIMARY KEY,
	machine_id INTEGER,
	status TEXT,
	timestamp DATETIME
);

CREATE TABLE admin (
	amindid INTEGER PRIMARY KEY,
	username TEXT,
	password TEXT
);

CREATE TABLE user (
	userid INTEGER PRIMARY KEY,
	username TEXT,
	password TEXT
);

CREATE TABLE configs (
	configid INTEGER PRIMARY KEY,
	machineid INTEGER,
	settings TEXT,
	timestamp DATETIME	
);
