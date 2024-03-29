import sys
import sqlite3
from typing import List

sys.path.append("../backend")
from database.orm.databaseObject import DatabaseObject
from database.orm.machine.machineProgram import MachineProgram
from database.orm.notification.warning import Warning
from database.orm.notification.error import Error
from database.orm.user.admin import Admin
from database.orm.machine.machineState import MachineState
from database.orm.program.programState import ProgramState
from database.orm.machine.protocol import Protocol
from database.handler.emptySetException import EmptySetException

class DatabaseHandler:

    #set up the connection to the database file and use a cusror for queries
    _CONNECTION = sqlite3.connect("database/machine-sim.db", check_same_thread=False)
    _CURSOR = _CONNECTION.cursor()
    
    
    @staticmethod
    def select(query: str, parameter: tuple = None) -> List[DatabaseObject]:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        if parameter == None:
            DatabaseHandler._CURSOR.execute(query)
        elif type(parameter[0]) == str:
            form = f"{parameter[0]}"
            DatabaseHandler._CURSOR.execute(query, (form,))
        else:
            DatabaseHandler._CURSOR.execute(query, parameter)
        resultSet: List[DatabaseObject] = DatabaseHandler._CURSOR.fetchall()
        DatabaseHandler._CURSOR.close()
        if(len(resultSet) == 0):
            raise EmptySetException()
        else:
            return resultSet
            
    
    def save(query: str, values: tuple) -> None:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        DatabaseHandler._CURSOR.execute(query, values)
        DatabaseHandler._CONNECTION.commit()
        DatabaseHandler._CURSOR.close()

    @staticmethod
    def delete(query: str, parameter: tuple = None) -> None:
        DatabaseHandler._CURSOR = DatabaseHandler._CONNECTION.cursor()
        if parameter == None:
            DatabaseHandler._CURSOR.execute(query)
        else:
            DatabaseHandler._CURSOR.execute(query, parameter)
        DatabaseHandler._CONNECTION.commit()
        DatabaseHandler._CURSOR.close()
    
    @staticmethod
    def selectMachineProgram(name: str) -> MachineProgram:
       try:
        resultSet: List[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_program WHERE machine_program_description= ?", (name,))
        return MachineProgram(*DatabaseObject(resultSet[0]).getResultRow())
       except EmptySetException as e:
           return None
   
    @staticmethod
    def selectAllMachinePrograms() -> List[MachineProgram]:
        resultSet: List[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_program")
        allProgramslist: List[MachineProgram] = []
        print(resultSet)
        for result in resultSet:
            allProgramslist.append(MachineProgram(*DatabaseObject(result).getResultRow()))
        return allProgramslist
    
    @staticmethod
    def selectMachineProgramById(id: str) -> MachineProgram:
        try:
            resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM machine_program WHERE machine_program_id= ?", (id,))
            return MachineProgram(*DatabaseObject(resultSet[0]).getResultRow())
        except EmptySetException as e:
            return None
    
    #get all possible warning messages within the Database
    @staticmethod
    def selectWarningMessages() -> List[Warning]:
        resultSet: List[Warning] = DatabaseHandler.select(f"SELECT * FROM warning")
        warningMessages: List[str] = []
        for result in resultSet:
            warning: Warning = Warning(DatabaseObject(result))
            warningMessages.append(warning)
        return warningMessages
    
    @staticmethod
    def selectErrorMessages() -> List[Error]:
        resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * FROM error")
        errorMessages: List[str] = []
        for result in resultSet:
            error: Error = Error(DatabaseObject(result))
            errorMessages.append(error)
        return errorMessages
    
    @staticmethod
    def selectAdminUsers() -> List[Admin]:
        resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * from admin")
        adminUsers: List[Admin] = []
        for result in resultSet:
            adminUser: Admin = Admin(DatabaseObject(result))
            adminUsers.append(adminUser)
        return adminUsers
    
    @staticmethod 
    def selectMachineStates() -> List[MachineState]:
        resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * from machine_state")
        machineStates: List[MachineState] = []
        print(resultSet)
        for result in resultSet:
            machineState: MachineState = MachineState(*DatabaseObject(result).getResultRow())
            machineStates.append(machineState)
        return machineStates
    
    @staticmethod
    def selectMachineState(id: int) -> MachineState:
        try:
            resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * from machine_state WHERE machine_state_id = ?", (id,))
            return MachineState(*DatabaseObject(resultSet[0]).getResultRow())
        except EmptySetException as e:
            return None
    
    @staticmethod
    def selectProgramState(id: int) -> ProgramState:
        try:
            resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * from program_state WHERE program_state_id = ?", (id,))
            listOfParameters: List[object] = DatabaseObject(resultSet[0]).getResultRow() 
            return ProgramState(*listOfParameters)
        except EmptySetException as e:
            return None
    
    @staticmethod
    def selectProtocolById(id: int) -> Protocol:
        try:
            resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * from machine_protocol WHERE machine_protocol_id= ?", (id,))
            listOfParameters: List[object] = DatabaseObject(resultSet[0]).getResultRow() 
            return Protocol(*listOfParameters)
        except EmptySetException as e:
            return None

    @staticmethod
    def selectProtocolByName(description: str) -> Protocol:
        try:
            resultSet: List[DatabaseObject] = DatabaseHandler.select(f"SELECT * from machine_protocol WHERE protocol_description= ?", (description,))
            listOfParameters: List[object] = DatabaseObject(resultSet[0]).getResultRow() 
            return Protocol(*listOfParameters)
        except EmptySetException as e:
            return None
    
    @staticmethod
    def storeMachineState(machineState: MachineState) -> None:
        query = "INSERT INTO machine_state " + \
            "(last_edited, machine_protocol, machine_state_name, error_state, warning_state, program_state, machine_start_time, machine_stop_time," + \
            "machine_down_time, machine_runtime, total_items, energy_consumption_watt, capacity_lasermodule, coolant_level) " + \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (machineState.getLastEdited(), machineState.getMachineProtocol(), machineState.getName(), machineState.getErrorState(), machineState.getWarningState(), 
                  machineState.getProgramState(), machineState.getMachineStartTime(), machineState.getMachineStopTime(), machineState.getMachineDownTime(), 
                  machineState.getMachineRuntime(), machineState.getAllItems(), machineState.getEnergyConsumptionWatt(), machineState.getCapacityLaserModule(), machineState.getCoolantLevelMl())
        DatabaseHandler.save(query, values)
        

    @staticmethod
    def storeProgramState(programState: ProgramState) -> None:
        query = "INSERT INTO program_state " + \
            "(program_id, program_target_amount, program_current_amount, program_runtime) " + \
            "VALUES (?, ?, ?, ?)"
        values = (programState.getID() , programState.getTargetAmount(), programState.getCurrentAmount(), programState.getRuntime())
        DatabaseHandler.save(query, values) 
        resultSet: List[DatabaseObject] = DatabaseHandler.select("SELECT * FROM program_state ORDER BY program_state_id DESC LIMIT 1")
        return DatabaseObject(resultSet[0]).getResultRow()[0]
    
    @staticmethod
    def deleteProgramState(id: int) -> None:
        programState: ProgramState = DatabaseHandler.selectProgramState(id)
        if(programState != None):
            DatabaseHandler.delete("DELETE FROM program_state WHERE program_state_id = ?", (id,))
    
    @staticmethod
    def deleteMachineStateById(id: int) -> None:
        machineState: MachineState = DatabaseHandler.selectMachineState(id)
        if(machineState != None):
            DatabaseHandler.delete("DELETE FROM machine_state WHERE machine_state_id = ?", (id,))
            DatabaseHandler.deleteProgramState(machineState.getProgramState())





    


