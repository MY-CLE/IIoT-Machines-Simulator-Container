from handler.databaseHandler import DatabaseHandler
from orm.machine.machineProgram import MachineProgram
from orm.databaseObject import DatabaseObject
from orm.program.programState import ProgramState
from orm.machine.machineState import MachineState
from orm.notification.error import Error
from orm.notification.warning import Warning
from orm.user.admin import Admin

result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_program;")
dbObj = DatabaseObject(result[0])
machine_program = MachineProgram(dbObj)
print(machine_program)    

result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_state;")
dbObj = DatabaseObject(result[0])
machine_state = MachineState(*dbObj.getResultRow())
print(machine_state)    

result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM program_state;")
dbObj = DatabaseObject(result[0])
program_state = ProgramState(dbObj)
print(program_state)    

result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM warning;")
dbObj = DatabaseObject(result[0])
warning = Warning(dbObj)
print(warning)    

result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM error;")
dbObj = DatabaseObject(result[0])
error = Error(dbObj)
print(error)    

result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM admin;")
dbObj = DatabaseObject(result[0])
admin = Admin(dbObj)
print(admin)    