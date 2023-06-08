import sqlite3
import sys

sys.path.append("../backend")
from database.orm.databaseObject import DatabaseObject
from database.orm.machine.machineProgram import MachineProgram
from database.orm.notification.warning import Warning
from database.orm.notification.error import Error
from database.orm.user.admin import Admin
from database.orm.machine.machineState import MachineState

class DatabaseHandler:

    _CONNECTION = sqlite3.connect("database/machine-sim.db")
    _CURSOR = _CONNECTION.cursor()


    @staticmethod
    def select(query: str, parameter: str = None) -> list[DatabaseObject]:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        if parameter == None:
            DatabaseHandler._CURSOR.execute(query)
        else:
            DatabaseHandler._CURSOR.execute(query, parameter)
        resultSet: list[DatabaseObject] = DatabaseHandler._CURSOR.fetchall()
        DatabaseHandler._CURSOR.close()
        return resultSet
    
    @staticmethod
    def selectMachineProgram(name: str) -> MachineProgram:
       resultSet: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_program WHERE machine_program_description = ?", (name,))
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
    
    @staticmethod
    def selectAdminUsers() -> list[Admin]:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * from admin")
        adminUsers: list[Admin] = []
        for result in resultSet:
            adminUser: Admin = Admin(DatabaseObject(result))
            adminUsers.append(adminUser)
        return adminUsers
    
    @staticmethod 
    def selectMachineStates() -> list[MachineState]:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * from machine_state")
        machineStates: list[MachineState] = []
        for result in resultSet:
            machineState: MachineState = MachineState(DatabaseObject(result))
            machineStates.append(machineState)
        return machineStates

    




