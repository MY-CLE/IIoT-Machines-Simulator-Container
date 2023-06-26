import os
import sys
import sqlite3
import unittest
from datetime import datetime

os.chdir("../backend/")
sys.path.append(os.getcwd())
from database.handler.databaseHandler import DatabaseHandler
from database.orm.machine.machineProgram import MachineProgram
from database.orm.notification.warning import Warning
from database.orm.notification.error import Error
from database.orm.user.admin import Admin
from database.orm.machine.machineState import MachineState
from database.orm.program.programState import ProgramState
from database.orm.machine.protocol import Protocol

class HandlerTest(unittest.TestCase):
    
    #setup the connection to the database and create a cursor before the tests are started d
    DB_PATH = "../backend/database/machine-sim.db"

    @classmethod
    def setUpClass(cls):
        HandlerTest.setUp(cls)

    @classmethod
    def tearDownClass(cls):
        HandlerTest.tearDown(cls)

    @staticmethod
    def create_and_populate_table():
        conn = sqlite3.connect(HandlerTest.DB_PATH, check_same_thread=False)
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

    def setUp(self):
        if os.path.exists(self.DB_PATH):
            with open(self.DB_PATH, 'w') as file:
                file.truncate()
        self.create_and_populate_table()
    
    def tearDown(self):
        with open(self.DB_PATH, 'w') as file:
            file.truncate()
        self.create_and_populate_table()

    # tests for all DB-Handler methods that use MachineProgram class
    
    def test_selectMachineProgramByExistingID(self) -> None:
        machineProgram: MachineProgram =  DatabaseHandler.selectMachineProgramById(1)
        self.assertNotEqual(machineProgram, None)
        self.assertEqual(machineProgram.getID(), 1)
    
    def test_selectMachineProgramByWrongID(self) -> None:
        machineProgram: MachineProgram = DatabaseHandler.selectMachineProgramById(100)
        self.assertEqual(machineProgram, None)

    def test_selectMachineProgramByName(self) -> None:
        machineProgram: MachineProgram = DatabaseHandler.selectMachineProgram('Circle')
        self.assertNotEqual(machineProgram, None)
        self.assertEqual(machineProgram.getDescription(), 'Circle')

    def test_selectMachineProgramByWrongName(self) -> None:
        machineProgram: MachineProgram = DatabaseHandler.selectMachineProgram('Wrong')
        self.assertEqual(machineProgram, None)

    def test_selectAllMachinePrograms(self) -> None:
        machinePrograms: list[MachineProgram] = DatabaseHandler.selectAllMachinePrograms()

        #ensure PK is in ascending order and objects match 
        pkValue: int = 0
        for machineProgram in machinePrograms:
            pkValue = pkValue + 1
            self.assertEqual(machineProgram.getID(), pkValue)
            self.assertEqual(machineProgram, DatabaseHandler.selectMachineProgramById(pkValue))
        
         #enusere highest PK matches rowcount in table
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSize: int = len(DatabaseHandler._CURSOR.execute("select * from machine_program").fetchall())
        DatabaseHandler._CURSOR.close()
        self.assertEqual(pkValue, resultSize)
            
    
    # tests for all DB-Handler methods that use Warning class

    def test_selectAllWaringMessages(self) -> None:
        warningMessages: list[Warning] = DatabaseHandler.selectWarningMessages()

        #ensure PK is in ascending order
        pkValue: int = 0
        for waningMessage in warningMessages:
            pkValue = pkValue + 1
            self.assertEqual(waningMessage.getID(), pkValue)
        
        #enusere highest PK matches rowcount in table
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSize: int = len(DatabaseHandler._CURSOR.execute("select * from warning").fetchall())
        DatabaseHandler._CURSOR.close()
        self.assertEqual(pkValue, resultSize)

    # test for alls DB-Handler methods that use Error class

    def test_selectAllErrorMessages(self) -> None:
        errorMessages: list[Error] = DatabaseHandler.selectErrorMessages()

        #ensure PK is in ascending order
        pkValue: int = 0
        for errorMessage in errorMessages:
            pkValue = pkValue + 1
            self.assertEqual(errorMessage.getID(), pkValue)
        
        #enusere highest PK matches rowcount in table
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSize: int = len(DatabaseHandler._CURSOR.execute("select * from error").fetchall())
        DatabaseHandler._CURSOR.close()
        self.assertEqual(pkValue, resultSize)

     # test for alls DB-Handler methods that use Admin class
    
    def test_selectAllAdminUsers(self) -> None:
        adminUsers: list[Admin] = DatabaseHandler.selectAdminUsers()

        #ensure PK is in ascending order
        pkValue: int = 0
        for adminUser in adminUsers:
            pkValue = pkValue + 1
            self.assertEqual(adminUser.getID(), pkValue)
        
        #enusere highest PK matches rowcount in table
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSize: int = len(DatabaseHandler._CURSOR.execute("select * from admin").fetchall())
        DatabaseHandler._CURSOR.close()
        self.assertEqual(pkValue, resultSize)

     # test for alls DB-Handler methods that use MachineState class

    def test_selectMachineStateByExistingID(self) -> None:
        machineState: MachineState = DatabaseHandler.selectMachineState(1)
        self.assertNotEqual(machineState, None)
        self.assertEqual(machineState.getId(), 1)

    def test_selectMachineStateByWrongID(self) -> None:
        machineState: MachineState = DatabaseHandler.selectMachineState(100)
        self.assertEqual(machineState, None)


    def test_selectAllMachineStates(self) -> None:
        machineStates: list[MachineState] = DatabaseHandler.selectMachineStates()

        #ensure PK is in ascending order and objects match
        pkValue: int = 0
        for machineState in machineStates:
            pkValue = pkValue + 1
            self.assertEqual(machineState.getId(), pkValue)
            self.assertEqual(machineState, DatabaseHandler.selectMachineState(pkValue))
        
        #enusere highest PK matches rowcount in table
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSize: int = len(DatabaseHandler._CURSOR.execute("select * from machine_state").fetchall())
        DatabaseHandler._CURSOR.close()
        self.assertEqual(pkValue, resultSize)

    def test_storeMachineState(self) -> None:
        #!!!!PK is set on AutoIncrement!!!!

        #get rowcount before insert
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeBefore: int = len(DatabaseHandler._CURSOR.execute("select * from machine_state").fetchall())
        DatabaseHandler._CURSOR.close()
        machine_state: MachineState = MachineState(
        machineStateID=resultSizeBefore+1,
        lastEdited=datetime(2023, 6, 24, 10, 0, 0),
        machineProtocol=2,
        machineStateName="Running",
        errorState=0,
        warningState=0,
        programState=1,
        machineStartTime=datetime(2023, 6, 24, 10, 0, 0),
        machineStopTime=datetime(2023, 6, 24, 18, 0, 0),
        machineDownTime=60,
        machineRunTime=480,
        totalItems=1000,
        energyConsumptionWatt=500,
        capacityLasermodule=100,
        coolantLevel=80)
        DatabaseHandler.storeMachineState(machine_state)

        #compare to rowcount after insert
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeAfter: int = len(DatabaseHandler._CURSOR.execute("select * from machine_state").fetchall())
        DatabaseHandler._CURSOR.close()
        self.assertEqual(resultSizeBefore + 1, resultSizeAfter)

        #select by PK and check if objects are equal
        self.assertEqual(machine_state, DatabaseHandler.selectMachineState(resultSizeAfter))

    def test_deleteMachineStateByExistingID(self) -> None:
        # get the number of entries in the machine_state table before deletion
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeBefore: int = len(DatabaseHandler._CURSOR.execute("select * from machine_state").fetchall())
        DatabaseHandler._CURSOR.close()

        # get the number of entries in the program_state table before deletion
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeBeforeProgramState: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()

        machineState: MachineState = MachineState (
        machineStateID=resultSizeBefore+1,
        lastEdited=datetime(2023, 6, 24, 10, 0, 0),
        machineProtocol=2,
        machineStateName="Running",
        errorState=0,
        warningState=0,
        programState=1,
        machineStartTime=datetime(2023, 6, 24, 10, 0, 0),
        machineStopTime=datetime(2023, 6, 24, 18, 0, 0),
        machineDownTime=60,
        machineRunTime=480,
        totalItems=1000,
        energyConsumptionWatt=500,
        capacityLasermodule=100,
        coolantLevel=80)

        #store the mock object and immediately delete it afterwards
        DatabaseHandler.storeMachineState(machineState)
        DatabaseHandler.deleteMachineStateById(machineState.getId())

        # get the number of entries in the machine_state table after deletion
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeAfter: int = len(DatabaseHandler._CURSOR.execute("select * from machine_state").fetchall())
        DatabaseHandler._CURSOR.close()

        # get the number of entries in the program_state table after deletion
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeAfterProgramState: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()

        #ensure the 
        self.assertEqual(resultSizeAfter, resultSizeBefore)
        self.assertEqual(DatabaseHandler.selectMachineState(machineState.getId()), None)

        #ensure also foreign key relationships are removed
        self.assertNotEqual(resultSizeBeforeProgramState, resultSizeAfterProgramState)

        
        
    def test_deleteMachineStateByWrongID(self) -> None:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeBefore: int = len(DatabaseHandler._CURSOR.execute("select * from machine_state").fetchall())
        DatabaseHandler._CURSOR.close()

        DatabaseHandler.deleteMachineStateById(1000)

        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeAfter: int = len(DatabaseHandler._CURSOR.execute("select * from machine_state").fetchall())
        DatabaseHandler._CURSOR.close()

        #ensure that the table does not lose any entries
        self.assertEqual(resultSizeBefore, resultSizeAfter)

    #test for alls DB-Handler methods that use ProgramState class

    def test_selectProgramStateByExisingID(self) -> None:
        programState: ProgramState = DatabaseHandler.selectProgramState(1)
        self.assertNotEqual(programState, None)
        self.assertEqual(programState.getID(), 1)

    def test_selectProgramStateByWrongID(self) -> None:
        programState: ProgramState = DatabaseHandler.selectProgramState(100)
        self.assertEqual(programState, None)
    
    def test_storePorgramState(self) -> None:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeBefore: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()

        programState: ProgramState = ProgramState(stateId=resultSizeBefore+1, id=100, targetAmount=500, currentAmount=250, runtime=120)
        DatabaseHandler.storeProgramState(programState)

        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeAfter: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()

        #ensure that one entry is added to the program_state table
        self.assertEqual(resultSizeAfter, resultSizeBefore + 1)
        self.assertEqual(programState, DatabaseHandler.selectProgramState(resultSizeAfter))
    
    def test_deleteProgramStateByExistingID(self) -> None:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeBefore: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()

        programState: ProgramState = ProgramState(stateId=resultSizeBefore+1, id=1, targetAmount=500, currentAmount=250, runtime=120)
        DatabaseHandler.storeProgramState(programState)
        DatabaseHandler.deleteProgramState(programState.getID())

        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeAfter: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()
        self.assertEqual(resultSizeAfter, resultSizeBefore)
        self.assertEqual(DatabaseHandler.selectProgramState(programState.getID()), None)

    def test_deleteProgramStateByWrongID(self) -> None:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeBefore: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()

        DatabaseHandler.deleteProgramState(1000)

        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        resultSizeAfter: int = len(DatabaseHandler._CURSOR.execute("select * from program_state").fetchall())
        DatabaseHandler._CURSOR.close()

        #ensure table does not lose any entries
        self.assertEqual(resultSizeAfter, resultSizeBefore)
    
    #test for alls DB-Handler methods that use Protocol class
    def test_selectProtocolByExistingID(self) -> None:
        protocol: Protocol =  DatabaseHandler.selectProtocolById(1)
        self.assertNotEqual(protocol, None)
        self.assertEqual(protocol.getProtocolID(), 1)
    
    def test_selectProtocolByWrongID(self) -> None:
        protocol: Protocol =  DatabaseHandler.selectProtocolById(1000)
        self.assertEqual(protocol, None)
    
    def test_selectProtocolByExistingName(self) -> None:
        protocol: Protocol = DatabaseHandler.selectProtocolByName('None')
        self.assertNotEqual(protocol, None)
        self.assertEqual(protocol.getProtocolDescription(), 'None')

    def test_selectProtocolByWrongName(self) -> None:
        protocol: Protocol = DatabaseHandler.selectProtocolByName('swtm ist das beste')
        self.assertEqual(protocol, None)



if __name__=='__main__':
    unittest.main()