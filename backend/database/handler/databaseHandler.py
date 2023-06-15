import sqlite3
import sys
import threading

sys.path.append("../backend")
from database.orm.databaseObject import DatabaseObject
from database.orm.machine.machineProgram import MachineProgram
from database.orm.notification.warning import Warning
from database.orm.notification.error import Error
from database.orm.user.admin import Admin
from database.orm.machine.machineState import MachineState
from database.orm.program.programState import ProgramState

class DatabaseHandler:

    #set up the connection to the database file and use a cusror for queries
    _CONNECTION = sqlite3.connect("database/machine-sim.db", check_same_thread=False)
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
    
    def save(query: str, values: tuple) -> None:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        DatabaseHandler._CURSOR.execute(query, values)
        DatabaseHandler._CONNECTION.commit()
        DatabaseHandler._CURSOR.close()
    
    @staticmethod
    def selectMachineProgram(name: str) -> MachineProgram:
       resultSet: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_program WHERE machine_program_description = ?", (name,))
       return MachineProgram(DatabaseObject(resultSet[0]))
   
    @staticmethod
    def selectAllMachinePrograms() -> list[MachineProgram]:
        resultSet: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_program")
        print(resultSet)
        allProgramslist: list[MachineProgram] = []
        for result in resultSet:
            allProgramslist.append(MachineProgram(DatabaseObject(result)))
        return allProgramslist
    
    @staticmethod
    def selectMachineProgramById(id: str) -> MachineProgram:
        print(id)
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM machine_program WHERE machine_program_id = '{id}'")
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
    
    @staticmethod
    def selectMachineState(id: int) -> MachineState:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * from machine_state WHERE machine_state_id = ?", (id,))
        return MachineState(DatabaseObject(resultSet[0]))
    
    @staticmethod
    def selectProgramState(id: int) -> ProgramState:
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * from program_state WHERE program_state_id = ?", (id,))
        return ProgramState(DatabaseObject(resultSet[0]))
    
    @staticmethod
    def storeMachineState(machineState: MachineState) -> None:
        query = "INSERT INTO machine_state " + \
            "(machine_state_name, error_state, warning_state, program_state, machine_start_time, machine_stop_time, machine_down_time, all_items, energy_consumption_watt, capacity_lasermodule, coolant_level) " + \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (machineState.getName(), machineState.getErrorState(), machineState.getWarningState(), machineState.getProgramState(), 
              machineState.getMachineStartTime(), machineState.getMachineStopTime(), machineState.getMachineDownTime(), machineState.getAllItems(), 
              machineState.getEnergyConsumptionWatt(), machineState.getCapacityLaserModule(), machineState.getCoolantLevelMl())
        DatabaseHandler.save(query, values)
        

    @staticmethod
    def storeProgramState(program_id, program_target_amount,program_current_amount,program_runtime) -> None:
        query = "INSERT INTO program_state " + \
            "(program_id, program_target_amount, program_current_amount, program_runtime) " + \
            "VALUES (?, ?, ?, ?)"
        values = (program_id , program_target_amount, program_current_amount, program_runtime)
        DatabaseHandler.save(query, values)
        resultSet: list[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM program_state WHERE program_id = ?", (programState.getID(),))
        return ProgramState(DatabaseObject(resultSet[0])).getStateID()



    


    


