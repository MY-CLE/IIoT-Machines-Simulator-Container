import os
import sys
import json
import sqlite3
import unittest
sys.path.append("..")
from backend.database.handler.databaseHandler import DatabaseHandler
from backend.logic.simulator import Simulator
from backend.app import app

simulator = Simulator()
class TestApi(unittest.TestCase):

    app.testing = True
    client = app.test_client()
    DB_PATH = "../backend/database/machine-sim.db"

    @classmethod
    def setUpClass(cls):
        if os.path.exists(cls.DB_PATH):
            with open(cls.DB_PATH, 'w') as file:
                file.truncate()
        cls.create_and_populate_table()

    @classmethod
    def tearDownClass(cls):
        with open(cls.DB_PATH, 'w') as file:
            file.truncate()
        cls.create_and_populate_table()

    @staticmethod
    def create_and_populate_table():
        conn = sqlite3.connect(TestApi.DB_PATH, check_same_thread=False)
        cursor = conn.cursor()

        with open("../backend/database/create_tables.sql", "r") as create_file:
            create_script = create_file.read()
            cursor.executescript(create_script)
            conn.commit()

        with open("../backend/database/populate_tables.sql", "r") as populate_file:
            populate_script = populate_file.read()
            cursor.executescript(populate_script)

        conn.commit()
        cursor.close()
        conn.close()

    def test_getSimulations(self):
        response = self.client.get('/api/simulations')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(json.dumps(response.json), r'{"simulations": \[\{"description": "[\w\s]+", "id": \d+, "last_edited": "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+"\}(?:, \{"description": "[\w\s]+", "id": \d+, "last_edited": "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+"\})*\]}')
    
    def test_postSimulation(self):
        # Save Simulation
        response = self.client.post('/api/simulations', data={'name': "Test"})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, "Simulation saved successfully")

    def test_putSimulation(self):
        # Create Simulation
        response = self.client.put('/api/simulations/0')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.text, "Simulation created successfully")
        # Load Simulation
        response = self.client.put('/api/simulations/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, simulator.loadSimulationById(1))

    def test_deleteSimulation(self):
        # Delete valid simulation id
        response = self.client.delete('/api/simulations/3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Simulation '3' was deleted successfully")

        # Delete invalid simulation id
        response = self.client.delete('/api/simulations/100')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Simulation '100' does not exist")
    
    def test_patchProtocol(self):
        # 'Modbus/TCP' protocol
        response = self.client.patch('/api/simulations/protocol', data={'protocol': "Modbus/TCP"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Protocol 'Modbus/TCP' was set successfully")

        # 'OPCUA' protocol
        response = self.client.patch('/api/simulations/protocol', data={'protocol': "OPCUA"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Protocol 'OPCUA' was set successfully")

        # 'None' protocol
        response = self.client.patch('/api/simulations/protocol', data={'protocol': "None"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Protocol 'None' was set successfully")
        
        # Invalid protocol
        response = self.client.patch('/api/simulations/protocol', data={'protocol': "InvalidProtocol"})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "Protocol 'InvalidProtocol' is not supported")

    def test_getMachine(self):
        response = self.client.get('/api/simulations/machine')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, simulator.simulatedMachine.getMachineStateSnapshot())

    def test_patchMachine(self):
        # Change machine state parameter as user
        response = self.client.patch('/api/simulations/machine', json={'id': 1,'description': "program_status", 'value': 2, 'isAdminParameter': False})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Machine state parameters updated successfully")

        # Change machine state parameter as admin
        response = self.client.patch('/api/simulations/machine', json={'id': 4,'description': "program_status", 'value': 2, 'isAdminParameter': True})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Machine state parameters updated successfully")

    def test_putMachineAuth(self):
        # Valid password
        response = self.client.put('/api/simulations/machine/auth', data={'password': 'admin123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Successefully authenticated")

        # Invalid password
        response = self.client.put('/api/simulations/machine/auth', data={'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.text, "Authentication failed")
    
    def test_getNotifications(self):
        response = self.client.get('/api/simulations/machine/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, simulator.notification.getNotificationsJSON())

    def test_postNotifications(self):
        # Invalid Error Id and Warning Id
        response = self.client.post('/api/simulations/machine/notifications', data={'error_id': '', 'warning_id': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "No Error Id or Warning Id provided")

        # Valid Error Id
        response = self.client.post('/api/simulations/machine/notifications', data={'error_id': 1, 'warning_id': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Error was successfully set")

        # Valid Warning Id
        response = self.client.post('/api/simulations/machine/notifications', data={'error_id': '', 'warning_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Warning was successfully set")

    def test_patchNotifications(self):
        response = self.client.patch('/api/simulations/machine/notifications')
        self.assertEqual(response.status_code, 200)                             
        self.assertEqual(response.text, "Errors and Warnings were successfully reset")

    def test_getMachinePrograms(self):
        # Get list of programs
        response = self.client.get('/api/simulations/machine/programs')
        self.assertEqual(response.status_code, 200)
        listOfPrograms = simulator.getPrograms()
        data = {"programs": []}
        for program in listOfPrograms:
            data["programs"].append(program.toJSON())
        self.assertEqual(response.json, data)

    def test_getCurrentMachinePrograms(self):
        # Get program state snapshot
        response = self.client.get('/api/simulations/machine/programs/current')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, simulator.simulatedProgram.getProgramStateSnapshot())

    def test_putCurrentMachinePrograms(self):
        # Set program
        response = self.client.put('/api/simulations/machine/programs/current', data={'program_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Program was successfully changed")

    def test_patchCurrentMachinePrograms(self):
        # Start program
        response = self.client.patch('/api/simulations/machine/programs/current', json={'id':"1",'description':"program_status",'value': "start"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Program was successfully started")

        # Stop program
        response = self.client.patch('/api/simulations/machine/programs/current', json={'id':"1",'description':"program_status",'value': "stop"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Program was successfully stopped")

        # Reset program
        response = self.client.patch('/api/simulations/machine/programs/current', json={'id':"1",'description':"program_status",'value': "reset"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Program was successfully reset")


if __name__ == '__main__':
    unittest.main()