import sqlite3
import sys

sys.path.append("../backend")
from database.orm.databaseObject import DatabaseObject
from database.orm.machine.machineProgram import MachineProgram
from database.orm.program.programState import ProgramState
from database.orm.notification.warning import Warning
from database.orm.notification.error import Error

class DatabaseHandler:

    #set up the connection to the database file and use a cusror for queries
    _CONNECTION = sqlite3.connect("database/machine-sim.db")
    _CURSOR = _CONNECTION.cursor()

    #execute a query with the cursor and return the result set in a list
    #close cursor when done
    @staticmethod
    def select(query: str) -> list[DatabaseObject]:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        DatabaseHandler._CURSOR.execute(query)
        resultSet: list[DatabaseObject] = DatabaseHandler._CURSOR.fetchall()
        DatabaseHandler._CURSOR.close()
        return resultSet

    #get programState out of the Database using the primary key of the table -> result is unique
    @staticmethod
    def selectProgramState(wId: int) -> ProgramState:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM program_state WHERE program_state_id = '{wId}'")
        return ProgramState(DatabaseObject(resultSet[0]))

    #get the machineProgram by name
    #return the first result of the query
    @staticmethod
    def selectMachineProgram(name: str) -> MachineProgram:
       resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM machine_program WHERE machine_program_description = '{name}'")
       return MachineProgram(DatabaseObject(resultSet[0]))
    
    @staticmethod
    def selectMachineProgramById(id: str) -> MachineProgram:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM machine_program WHERE machine_prorgram_id = '{id}'")
        return MachineProgram(DatabaseObject(resultSet[0]))
    
    #get all possible warning messages within the Database
    @staticmethod
    def selectWarningMessages() -> list[str]:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM warning")
        warningMessages: list[str] = []
        for result in resultSet:
            warning: Warning = Warning(DatabaseObject(result))
            warningMessages.append(warning.getType())
        return warningMessages
    
     #get all possible error messages within the Database
    @staticmethod
    def selectErrorMessages() -> list[str]:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM error")
        errorMessages: list[str] = []
        for result in resultSet:
            error: Error = Error(DatabaseObject(result))
            errorMessages.append(error.getType())
        return errorMessages



