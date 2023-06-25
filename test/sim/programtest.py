import logging
import unittest
import sys
sys.path.append("..")
from backend.database.handler.databaseHandler import DatabaseHandler
from backend.database.orm.program.programState import ProgramState
from backend.database.orm.machine.machineProgram import MachineProgram
from datetime import datetime
from unittest.mock import patch
from backend.logic.program import Program

class TestProgram(unittest.TestCase):
    def setUp(self) -> None:
        self.program: Program = Program()

    def test_LoadProgramState(self) -> None:
        programState: ProgramState = ProgramState(stateId=1, id=1, targetAmount=1, currentAmount=0, runtime=0)
        machineProgram: MachineProgram = MachineProgram(ID=1, description="Test", laserModuleWeardown=1, coolantConsumptionMl=1, powerConsumptionLaserModule=1, timePerItem=1)

        #mock object to check if loadMachineProgram gets called
        with patch.object(Program, 'loadMachineProgram', return_value=None) as mock_load:
            self.program.loadProgramState(programState)

            self.assertEqual(self.program.programId, programState.getID())
            self.assertEqual(self.program.programTargetAmount, programState.getTargetAmount())
            self.assertEqual(self.program.programCurrentAmount, programState.getCurrentAmount())
            self.assertEqual(self.program.programRuntime, programState.getRuntime())
            self.assertIsNone(self.program.lastUpdate)

            mock_load.assert_called_once()


    def test_LoadMachineStateProgram(self) -> None:
        programState: ProgramState = ProgramState(stateId=1, id=1, targetAmount=1, currentAmount=0, runtime=0)
        machineProgram: MachineProgram = MachineProgram(ID=1, description="Test", laserModuleWeardown=1, coolantConsumptionMl=1, powerConsumptionLaserModule=1, timePerItem=1)
        self.machineProgram =  DatabaseHandler.selectMachineProgramById(programState.getID())

        self.program.setMachineProgram(machineProgram)
        self.program.loadMachineProgram()

        self.assertFalse(self.program.isProgramRunning)
        self.assertEqual(self.program.programRuntime, 0)
        self.assertEqual(self.program.programId, machineProgram.getID())
        self.assertEqual(self.program.programProgramDescription, machineProgram.getDescription())
        self.assertEqual(self.program.programLaserModuleWeardown, machineProgram.getLaserModuleWeardown()*0.01)
        self.assertEqual(self.program.programCoolantConsumption, machineProgram.getCoolantConsumption()*0.01)
        self.assertEqual(self.program.programLaserModulePowerConsumption, machineProgram.getLaserModulePowerConsumption())
        self.assertEqual(self.program.programTimePerItem, machineProgram.getTimePerItem()) 


    def test_UpdateProgram(self) -> None:
        newTime: datetime = datetime.now()

        self.program.startProgram(newTime)

        result = self.program.updateProgram(newTime)

        self.assertEqual(result[0], self.program.programLaserModulePowerConsumption)
        self.assertEqual(result[1], self.program.programCoolantConsumption)
        self.assertEqual(result[2], self.program.newItems)
        self.assertEqual(result[3], self.program.isProgramRunning)
        self.assertEqual(result[4], self.program.programLaserModuleWeardown)
        self.assertEqual(result[5], self.program.additionalTime)

        #program just started so currentAmount/addtionalTime should be 0
        self.assertEqual(self.program.programCurrentAmount, 0)
        self.assertEqual(self.program.additionalTime, 0)

        self.assertTrue(self.program.isProgramRunning)

    def test_CalculateProgramRuntime(self) -> None:
        nowTime: datetime = datetime.now()

        self.program.startProgram(nowTime)
        self.program.calculateProgramRuntime(nowTime)

        self.assertEqual(self.program.lastUpdate, nowTime)

        #program was just started so additionalTime has to be 0
        self.assertEqual(self.program.additionalTime, 0)

        #program time since the last update should be the time difference between nowTime and programStartTime
        expectedTimeSinceLastUpdate = (nowTime - self.program.programStartTime).total_seconds()
        self.assertEqual(self.program.programTimeSinceLastUpdate, expectedTimeSinceLastUpdate)

        #program runtime should be updated with the programTimeSinceLastUpdate
        expectedRuntime = self.program.programTimeSinceLastUpdate
        self.assertEqual(self.program.programRuntime, expectedRuntime)

    def test_UpdateProgramCurrentAmount(self) -> None:
        nowTime: datetime = datetime.now()

        self.program.startProgram(nowTime)
        self.program.calculateProgramRuntime(nowTime)

        self.program.updateProgramCurrentAmount()

        expectedNewItems = self.program.programTimeSinceLastUpdate / self.program.programTimePerItem
        expectedProgramCurrentAmount = self.program.programCurrentAmount + self.program.newItems
        self.assertEqual(self.program.newItems, expectedNewItems)
        self.assertEqual(self.program.programCurrentAmount, expectedProgramCurrentAmount)

    def test_UpdateProgramLaserModulePowerConsumption(self) -> None:
        nowTime: datetime = datetime.now()

        self.program.startProgram(nowTime)
        self.program.calculateProgramRuntime(nowTime)

        self.program.updateProgramLaserModulePowerConsumption()

        expectedLaserModulePowerConsumption = self.program.programLaserModulePowerConsumption + self.program.programTimeSinceLastUpdate / self.program.programTimePerItem

        self.assertEqual(self.program.programLaserModulePowerConsumption, expectedLaserModulePowerConsumption)

    def test_ResetProgram(self) -> None:
        #mock object for laodMachineProgram so we can make sure it only gets called once
        with patch.object(self.program, 'loadMachineProgram') as mock_load:
            self.program.resetProgram()

            self.assertFalse(self.program.isProgramRunning)
            mock_load.assert_called_once()

    def test_ResetToDefaultState(self) -> None:
        self.program.resetToDefaultState()

        self.assertEqual(self.program.programCurrentAmount, 0)
        self.assertEqual(self.program.programRuntime, 0)
        self.assertEqual(self.program.programLaserModulePowerConsumption, 0)

        self.assertIsNone(self.program.programId)
        self.assertFalse(self.program.isProgramRunning)
        self.assertEqual(self.program.programTargetAmount, 100)
        self.assertIsNone(self.program.programMachineProgramId)
        self.assertEqual(self.program.programProgramDescription, "")
        self.assertEqual(self.program.programLaserModuleWeardown, 0)
        self.assertEqual(self.program.programCoolantConsumption, 0)
        self.assertEqual(self.program.programTimePerItem, 1)
        self.assertEqual(self.program.newItems, 0)

        self.assertIsNone(self.program.machineProgram)

        self.assertIsNone(self.program.programStartTime)
        self.assertIsNone(self.program.programStopTime)
        self.assertIsNone(self.program.programTimeSinceLastUpdate)
        self.assertIsNone(self.program.lastUpdate)
        self.assertEqual(self.program.additionalTime, 0)

    def test_SetMachineProgram(self) -> None:
        machineProgram: MachineProgram = MachineProgram(ID=1, description="Test", laserModuleWeardown=1, coolantConsumptionMl=1, powerConsumptionLaserModule=1, timePerItem=1)

        #mock object for setMachineProgram so we can make sure it only gets called once
        with patch.object(self.program, 'setMachineProgram') as mock_load:
            self.program.setMachineProgram(machineProgram)

            mock_load.assert_called_once()

    def test_StartProgram(self) -> None:
        startTime = datetime.now()

        self.program.startProgram(startTime)

        self.assertEqual(self.program.programStartTime, startTime)
        self.assertTrue(self.program.isProgramRunning)

    def test_StopProgram(self) -> None:
        stopTime = datetime.now()

        self.program.stopProgram(stopTime)

        self.assertFalse(self.program.isProgramRunning)
        self.assertEqual(self.program.programStopTime, stopTime)
        self.assertIsNone(self.program.lastUpdate)

    def test_CheckMachineRuntimeValue(self) -> None:
        machineRuntime = 5
        self.program.setProgramRuntime(10)

        self.program.checkMachineRuntimeValue(machineRuntime)

        self.assertEqual(self.program.programRuntime, machineRuntime)

if __name__ == '__main__':
    unittest.main() 