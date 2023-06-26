-- Populating admin table
INSERT INTO admin (admin_password)
VALUES ('admin123');

-- Populating machine_state table
INSERT INTO machine_state (last_edited, machine_protocol, machine_state_name, error_state, warning_state, program_state, machine_start_time, machine_stop_time, machine_down_time, machine_runtime, total_items, energy_consumption_watt, capacity_lasermodule, coolant_level)
VALUES ('2023-06-15 09:00:00.000000', 1, 'State 1', 2, 3, 1, '2023-06-15 08:30:00.000000', '2023-06-15 10:30:00.000000', 60, 7200, 100, 5000, 200, 80),
	('2023-06-15 10:30:00.000000', 2, 'State 2', 3, 4, 2, '2023-06-15 10:00:00.000000', '2023-06-15 12:00:00.000000', 120, 10800, 150, 6000, 250, 70),
	('2023-06-15 12:30:00.000000', 3, 'State 3', 4, 5, 3, '2023-06-15 12:00:00.000000', '2023-06-15 14:00:00.000000', 90, 14400, 200, 7000, 300, 60);


-- Populating machine_program table
INSERT INTO machine_program (machine_program_description, program_laser_module_weardown, program_coolant_consumption_ml, program_laser_power_consumption_watt, program_time_per_item)
VALUES ('Circle', 1, 5, 3000, 10),
       ('Triangle', 3, 10, 3500, 15),
       ('Rectangle', 2, 2, 2000, 5);

-- Populating error table
INSERT INTO error (error_type)
VALUES ('Coolant empty. Machine is stopping!'),
       ('Laser module burnt out. Machine is stopping!'),
       ('Safety door is open! Close it.');

-- Populating program_state table
INSERT INTO program_state (program_id, program_target_amount, program_current_amount, program_runtime)
VALUES (1, 50, 25, 5),
       (2, 100, 75, 6),
       (3, 200, 150, 7);

-- Populating warning table
INSERT INTO warning (warning_type)
VALUES ('Coolant Level below 10%. Please refill!'),
       ('Laser module power below 10%. Please swap module!'),
       ('Power Consumption is high.');

INSERT INTO machine_protocol (protocol_description)
VALUES ('None'), 
       ('Modbus/TCP'),
       ('OPCUA')


