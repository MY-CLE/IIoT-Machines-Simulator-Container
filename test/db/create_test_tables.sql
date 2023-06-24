CREATE TABLE admin (
	admin_id integer PRIMARY KEY AUTOINCREMENT,
	admin_password text
);

CREATE TABLE machine_state (
	machine_state_id integer PRIMARY KEY AUTOINCREMENT,
	last_edited timestamp,
	machine_protocol integer,
	machine_state_name text,
	error_state integer,
	warning_state integer,
	program_state integer,
	machine_start_time timestamp,
	machine_stop_time timestamp,
	machine_down_time integer,
	machine_runtime integer,
	total_items integer,
	energy_consumption_watt integer,
	capacity_lasermodule integer,
	coolant_level integer,
	FOREIGN KEY(error_state) REFERENCES error(error_id),
	FOREIGN KEY(warning_state) REFERENCES warning(warning_id),
	FOREIGN KEY(program_state) REFERENCES program_state(program_state_id),
	FOREIGN KEY(machine_protocol) REFERENCES machine_protocol(machine_protocol_id)
);

CREATE TABLE program_state (
	program_state_id integer PRIMARY KEY AUTOINCREMENT,
	program_id integer,
	program_target_amount integer,
	program_current_amount integer,
	program_runtime integer,
	FOREIGN KEY(program_id) REFERENCES machine_program(machine_program_id)
);

CREATE TABLE machine_program (
	machine_program_id integer PRIMARY KEY AUTOINCREMENT,
	machine_program_description text,
	program_laser_module_weardown integer, 
	program_coolant_consumption_ml integer,
	program_laser_power_consumption_watt integer,
	program_time_per_item integer
);

CREATE TABLE error (
	error_id integer PRIMARY KEY AUTOINCREMENT,
	error_type text
);

CREATE TABLE warning (
	warning_id integer PRIMARY KEY AUTOINCREMENT,
	warning_type text
);

CREATE TABLE machine_protocol (
	machine_protocol_id integer PRIMARY KEY AUTOINCREMENT,
	protocol_description text
);