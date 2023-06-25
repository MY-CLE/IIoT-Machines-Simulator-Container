import logging
import unittest
import sys
sys.path.append("..")
from backend.database.handler.databaseHandler import DatabaseHandler
from backend.database.orm.machine.machineState import MachineState
from datetime import datetime, timedelta
from unittest.mock import patch
from backend.logic.machine import Machine

class TestMachine(unittest.TestCase):
    def setUp(self):
        self.machine = Machine()

    def test_CalculateTimes(self) -> None:
        nowTime = datetime.now()

        self.machine.startMachine(nowTime - timedelta(seconds = 10))
        
        self.machine.calculateTimes(nowTime)

        expectedRuntime = 10
        expectedLastUpdate = nowTime
        self.assertEqual(self.machine.machineRuntime, expectedRuntime)
        self.assertEqual(self.machine.lastUpdate, expectedLastUpdate)
       
    def test_CalculateIdleTime(self) -> None:
        nowTime = datetime.now()

        self.machine.startMachine(nowTime - timedelta(seconds=10))
        self.machine.stopMachine(nowTime - timedelta(seconds=5))

        self.machine.calculateIdleTime(nowTime)

        expectedIdleTime = 5
        self.assertEqual(self.machine.machineIdleTime, expectedIdleTime)

    def test_StartMachine(self) -> None:
        startTime = datetime.now()

        self.machine.startMachine(startTime)

        self.assertEqual(self.machine.machineStartTime, startTime)
        self.assertEqual(self.machine.machineStopTime, startTime)
        self.assertTrue(self.machine.isMachineRunning)

    def test_StopMachine(self) -> None:
        stopTime = datetime.now()

        self.machine.stopMachine(stopTime)

        self.assertEqual(self.machine.machineStopTime, stopTime)
        self.assertFalse(self.machine.isMachineRunning)

    def test_ResetMachine(self) -> None:
        nowTime = datetime.now()
        
        self.machine.resetMachine()

        self.assertFalse(self.machine.isProgramRunning)
        self.assertEqual(self.machine.machineRuntime, 0)
        self.assertEqual(self.machine.totalItems, 0)
        self.assertEqual(self.machine.capacityLaserModule, 100)
        self.assertEqual(self.machine.totalEnergyConsumption, 0)
        self.assertEqual(self.machine.coolantLevel, 100)
        self.assertEqual(self.machine.machineStartTime, nowTime)

    def test_UpdateMachineErrors(self) -> None:
        # Define new errors and warnings
        newErrors = ["Hello", "No! Error"]
        newWarnings = ["Goodbye", "No! Warning"]

        # Use assertLogs as a context manager to capture logging output at the INFO level
        with self.assertLogs(level=logging.INFO) as cm:
            self.machine.updateMachineErrors(newErrors, newWarnings)

            # Check if the machine's active errors and warnings have been updated correctly
            self.assertEqual(self.machine.activeErrors, newErrors)
            self.assertEqual(self.machine.activeWarnings, newWarnings)

            # Define the expected logging output
            expectedLogging = [
                "INFO:root:Errors: " + str(newErrors),
                "INFO:root:Warnings: " + str(newWarnings)
            ]

            # Check if the output matches the expected value
            self.assertEqual(cm.output, expectedLogging)

    def test_UpdateMachine(self) -> None:
        nowTime: datetime = datetime.now()
        powerConsumptionPerS: int = 2
        coolantConsumptionPerS: int = 2
        newItems: int = 2
        isProgramRunning: bool = True
        laserModuleWeardown: float = 0.01
        programAdditionalTime = 2

        self.machine.startMachine(nowTime)
        machineRuntime = self.machine.updateMachine(nowTime, powerConsumptionPerS, coolantConsumptionPerS, newItems, isProgramRunning, laserModuleWeardown, programAdditionalTime)
        
        self.assertTrue(self.machine.isProgramRunning)
        self.assertEqual(self.machine.additionalTime, 0) #has to be null because calculateTimes sets addtionalTime to 0 when called in this case
        self.assertEqual(self.machine.machineRuntime, programAdditionalTime)
        self.assertEqual(self.machine.totalItems, newItems)
        self.assertEqual(self.machine.totalEnergyConsumption, powerConsumptionPerS * self.machine.timeSinceLastUpdate)
        self.assertEqual(self.machine.coolantLevel, 100 - coolantConsumptionPerS * self.machine.timeSinceLastUpdate)
        self.assertEqual(self.machine.capacityLaserModule, 100 - laserModuleWeardown * self.machine.timeSinceLastUpdate)

        self.assertEqual(self.machine.machineRuntime, machineRuntime)

    def test_LoadMachineState(self) -> None:
        nowTime: datetime = datetime.now()
        machineState: MachineState = MachineState(1, nowTime, 1, "TestMachine", 1, 1, 1, nowTime, nowTime, 1, 1, 1, 1, 1, 1)
        
        self.machine.loadMachineState(machineState)

        self.assertFalse(self.machine.isProgramRunning)
        self.assertEqual(self.machine.machineStateId, machineState.getID())
        self.assertEqual(self.machine.machineStateName, machineState.getName())
        self.assertEqual(self.machine.lastEdited, machineState.getLastEdited())
        self.assertEqual(self.machine.errorStateId, machineState.getErrorState())
        self.assertEqual(self.machine.warningStateId, machineState.getWarningState())
        self.assertEqual(self.machine.programStateId, machineState.getProgramState())
        self.assertEqual(self.machine.machineProtocolId, machineState.getMachineProtocol())
        self.assertEqual(self.machine.machineStartTime, machineState.getMachineStartTime())
        self.assertEqual(self.machine.machineStopTime, machineState.getMachineStopTime())
        self.assertEqual(self.machine.machineIdleTime, machineState.getMachineDownTime())
        self.assertEqual(self.machine.machineRuntime, machineState.getMachineRuntime())
        self.assertEqual(self.machine.totalItems, machineState.getAllItems())
        self.assertEqual(self.machine.coolantLevel, machineState.getCoolantLevelMl())
        self.assertEqual(self.machine.totalEnergyConsumption, machineState.getEnergyConsumptionWatt())
        self.assertEqual(self.machine.capacityLaserModule, machineState.getCapacityLaserModule())

    def test_ToDict(self) -> None:
        self.machine.machineStateId = 1
        self.machine.machineStateName = "Test Machine"
        self.machine.machineProtocolId = 1
        self.machine.lastEdited = "2023-06-25 12:00:00"
        self.machine.errorStateId = 2
        self.machine.warningStateId = 3
        self.machine.programStateId = 4
        self.machine.machineStartTime = "2023-06-25 10:00:00"
        self.machine.machineStopTime = "2023-06-25 11:00:00"
        self.machine.machineIdleTime = 3600
        self.machine.machineRuntime = 3600
        self.machine.totalItems = 10
        self.machine.totalEnergyConsumption = 50.0
        self.machine.capacityLaserModule = 100
        self.machine.coolantLevel = 80.0

        expectedDict = {
            "machineStateId": 1,
            "machineStateName": "Test Machine",
            "machineProtocolId": 1,
            "lastEdited": "2023-06-25 12:00:00",
            "errorStateId": 2,
            "warningStateId": 3,
            "programStateId": 4,
            "machineStartTime": "2023-06-25 10:00:00",
            "machineStopTime": "2023-06-25 11:00:00",
            "machineIdleTime": 3600,
            "machineRuntime": 3600,
            "totalItems": 10,
            "totalEnergyConsumption": 50.0,
            "capacityLaserModule": 100,
            "coolantLevel": 80.0
        }
        actualDict = self.machine.toDict()
        self.assertDictEqual(actualDict, expectedDict)

    def test_GetMachineStateSnapshot(self) -> None:
        self.machine.machineStateId = 1
        self.machine.machineStateName = "Test Machine"
        self.machine.machineProtocolId = 1
        self.machine.lastEdited = "2023-06-25 12:00:00"
        self.machine.machineRuntime = 3600
        self.machine.machineIdleTime = 1800
        self.machine.coolantLevel = 75
        self.machine.totalEnergyConsumption = 100.0
        self.machine.capacityLaserModule = 80
        self.machine.totalItems = 50
        self.machine.activeErrors = ["Error 1", "Error 2"]
        self.machine.activeWarnings = ["Warning 1", "Warning 2"]

        expectedData = {
            "machineStateId": 1,
            "machineStateName": "Test Machine",
            "machineProtocolId": 1,
            "lastEdited": "2023-06-25 12:00:00",
            "parameters": [
                {"id": "1", "description": "Runtime (s)", "value": 3600},
                {"id": "2", "description": "Idle Time (s)", "value": 1800},
                {"id": "3", "description": "Coolant Level (%)", "value": 75},
                {"id": "4", "description": "Power Consumption (Wh)", "value": 100},
                {"id": "5", "description": "Capacity Laser Module (%)", "value": 80},
                {"id": "6", "description": "Total Items", "value": 50}
            ],
            "error_state": {
                "errors": [
                    {"id": "0", "name": "Error 1"},
                    {"id": "1", "name": "Error 2"}
                ],
                "warnings": [
                    {"id": "0", "name": "Warning 1"},
                    {"id": "1", "name": "Warning 2"}
                ]
            }
        }
        actualData = self.machine.getMachineStateSnapshot()
        self.assertDictEqual(actualData, expectedData)

    def test_PrepareForDB(self) -> None:
        nowTime = datetime.now()
        machineStateName = "Test Machine"
        machineProtocolId = 1
        programStateId = 1

        self.machine.prepareForDB(nowTime, machineStateName, machineProtocolId, programStateId)

        self.assertEqual(self.machine.lastEdited, nowTime)
        self.assertEqual(self.machine.machineStateName, machineStateName)
        self.assertEqual(self.machine.machineProtocolId, machineProtocolId)
        self.assertEqual(self.machine.programStateId, programStateId)


if __name__ == '__main__':
    unittest.main() 