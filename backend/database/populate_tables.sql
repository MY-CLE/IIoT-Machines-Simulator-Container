-- Populating admin table
INSERT INTO admin (admin_password)
VALUES ('admin123');

-- Populating machine_state table
INSERT INTO machine_state (machine_state_name, error_state, warning_state, program_state, machine_start_time, machine_stop_time, machine_down_time, all_items, energy_consumption_watt, capacity_lasermodule, coolant_level)
VALUES ('Machine 1', 0, 0, 1, '2023-05-20 09:00:00', '2023-05-20 18:00:00', 20, 100, 5000, 80.5, 70.2),
       ('Machine 2', 1, 1, 0, '2023-05-20 10:30:00', '2023-05-20 19:30:00', 30, 200, 8000, 100.0, 60.7);

-- Populating machine_program table
INSERT INTO machine_program (machine_program_description, laser_module_weardown, coolant_consumption_ml, power_consumption_kwh, program_time_per_item)
VALUES ('Circle', 2000, 50.5, 0.5, 10),
       ('Triangle', 3000, 75.2, 0.7, 15),
       ('Rectangle', 4000, 100.0, 0.9, 12);

-- Populating error table
INSERT INTO error (error_type)
VALUES ('Coolant empty. Machine is stopping!'),
       ('Laser module burnt out. Machine is stopping!'),
       ('Power consumption significantly too high. Machine is stopping!');

-- Populating program_state table
INSERT INTO program_state (program_id, program_target_amount, program_current_amount, program_runtime)
VALUES (1, 50, 25, 5),
       (2, 100, 75, 6),
       (3, 200, 150, 7);
VALUES (1, 50, 25, '04:30:00'),
       (2, 100, 75, '06:15:00'),
       (3, 200, 150, '09:45:00');

-- Populating warning table
INSERT INTO warning (warning_type)
VALUES ('Coolant Level below 10%. Please refill!'),
       ('Laser module power below 10%. Please swap module!'),
       ('Power Consumption is getting high. Please take a break!');
