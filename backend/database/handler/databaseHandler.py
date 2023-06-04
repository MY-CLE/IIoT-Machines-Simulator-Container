import sqlite3
import sys

sys.path.append("../backend")
from database.orm.databaseObject import DatabaseObject
from database.orm.machine.machineProgram import MachineProgram
from database.orm.program.programState import ProgramState
from database.orm.notification.warning import Warning
from database.orm.notification.error import Error

class DatabaseHandler:

    _CONNECTION = sqlite3.connect("database/machine-sim.db")
    _CURSOR = _CONNECTION.cursor()

    @staticmethod
    def selectProgramState(wId: int) -> ProgramState:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM program_state WHERE program_state_id = '{wId}'")
        return ProgramState(DatabaseObject(resultSet[0]))

    @staticmethod
    def select(query: str) -> list[DatabaseObject]:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        DatabaseHandler._CURSOR.execute(query)
        resultSet: list[DatabaseObject] = DatabaseHandler._CURSOR.fetchall()
        DatabaseHandler._CURSOR.close()
        return resultSet
    
    @staticmethod
    def selectMachineProgram(name: str) -> MachineProgram:
       resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM machine_program WHERE machine_program_description = '{name}'")
       return MachineProgram(DatabaseObject(resultSet[0]))
    
    @staticmethod
    def selectWarningMessages() -> list[str]:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM warning")
        warningMessages: list[str] = []
        for result in resultSet:
            warning: Warning = Warning(DatabaseObject(result))
            warningMessages.append(warning.getType())
        return warningMessages
    
    @staticmethod
    def selectErrorMessages() -> list[str]:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM error")
        errorMessages: list[str] = []
        for result in resultSet:
            error: Error = Error(DatabaseObject(result))
            errorMessages.append(error.getType())
        return errorMessages



