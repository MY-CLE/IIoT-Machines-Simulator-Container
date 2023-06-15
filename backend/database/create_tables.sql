CREATE TABLE admin (
	admin_id integer PRIMARY KEY AUTOINCREMENT,
	admin_password text
);

CREATE TABLE machine_state (
	machine_state_id integer PRIMARY KEY AUTOINCREMENT,
	machine_state_name text,
	program_state integer,
	machine_start_time timestamp,
	machine_stop_time timestamp,
	machine_down_time integer,
	all_items integer,
	energy_consumption_watt integer,
	capacity_lasermodule float,
	coolant_level float,
	FOREIGN KEY(program_state) REFERENCES program_state(program_state_id)
);

CREATE TABLE program_state (
	program_state_id integer PRIMARY KEY AUTOINCREMENT,
	program_id integer,
	program_target_amount integer,
	program_current_amount integer,
	program_runtime integer
);

CREATE TABLE machine_program (
	machine_program_id integer PRIMARY KEY AUTOINCREMENT,
	machine_program_description text,
	laser_module_weardown integer, 
	coolant_consumption_ml integer,
	power_consumption_kwh integer,
	program_time_per_item float
);

CREATE TABLE error (
	error_id integer PRIMARY KEY AUTOINCREMENT,
	error_type text
);

CREATE TABLE warning (
	warning_id integer PRIMARY KEY AUTOINCREMENT,
	warning_type text
);