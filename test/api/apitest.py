import sys
import json
import unittest
sys.path.append("..")
from backend.database.handler.databaseHandler import DatabaseHandler
from backend.logic.simulator import Simulator
from backend.app import app

simulator = Simulator()
class TestApi(unittest.TestCase):

    app.testing = True
    client = app.test_client()

    def test_getSimulations(self):
        response = self.client.get('/api/simulations')
        self.assertEqual(response.status_code, 200)
        self.assertRegex(json.dumps(response.json), r'{"simulations": \[\{"description": "[\w\s]+", "id": \d+, "last_edited": "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+"\}(?:, \{"description": "[\w\s]+", "id": \d+, "last_edited": "\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+"\})*\]}')
        """def test_postSimulation(self):
        response = self.client.post('/api/simulations', data={'name': 'Test'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data, "Simulation saved successfully") """

    def test_putSimulation(self):
        response = self.client.put('/api/simulations/1')
        self.assertEqual(response.status_code, 200)

    """ def test_deleteSimulation(self):
        response = self.client.delete('/api/simulations/4')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Simulation '4' was deleted successfully") """
    
    def test_patchProtocol(self):
        response = self.client.patch('/api/simulations/protocol', data={'protocol': 'Modbus'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Protocol 'Modbus' was set successfully")

    def test_getMachine(self):
        response = self.client.get('/api/simulations/machine')
        self.assertEqual(response.status_code, 200)
        #self.assertRegex(json.dumps(response.json), r'\{"errorState": \{"errors": \[\], "warnings": \[\]\}, "lastEdited": null, "machineProtocolId": null, "machineStateId": null, "machineStateName": null, "parameters": \[\{"description": "[\w\s]+", "id": "\d+", "isAdminParameter": (?:true|false), "value": \d+}(?:, \{"description": "[\w\s]+", "id": "\d+", "isAdminParameter": (?:true|false), "value": \d+})*\]\}')


    def test_patchMachine(self):
        response = self.client.patch('/api/simulations/machine', json={'parameters': {'parameter1': 1, 'parameter2': 2}})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Machine state parameters updated successfully")

    def test_putMachineAuth(self):
        # Valid password
        response = self.client.put('/api/simulations/machine/auth', data={'password': 'admin123'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Successefully authenticated")

        # Invalid password
        response = self.client.put('/api/simulations/machine/auth', data={'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data, b"Authentication failed")
    
    def test_getNotifications(self):
        response = self.client.get('/api/simulations/machine/notifications')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, simulator.notification.getNotificationsJSON())

    def test_postNotifications(self):
        response = self.client.post('/api/simulations/machine/notifications', data={'error_id': '', 'warning_id': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.text, "No Error Id or Warning Id provided")

        response = self.client.post('/api/simulations/machine/notifications', data={'error_id': 1, 'warning_id': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Error was successfully set")

        response = self.client.post('/api/simulations/machine/notifications', data={'error_id': '', 'warning_id': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "Warning was successfully set")

    def test_patchNotifications(self):
        response = self.client.patch('/api/simulations/machine/notifications')
        self.assertEqual(response.status_code, 200)                             
        self.assertEqual(response.text, "Errors and Warnings were successfully reset")





if __name__ == '__main__':
    unittest.main()