from handler.databaseHandler import DatabaseHandler
from orm.machineProgram import MachineProgram
from orm.databaseObject import DatabaseObject
from orm.programState import ProgramState

print(DatabaseHandler.select("SELECT * FROM machine_program"))
result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM program_state;")
dbObj = DatabaseObject(result[0])
prSt = ProgramState(dbObj)
print(prSt)