from handler.databaseHandler import DatabaseHandler
from orm.machine_program import MachineProgram
from orm.databaseObject import DatabaseObject

print(DatabaseHandler.select("SELECT * FROM machine_program"))
result: list[DatabaseObject] = DatabaseHandler.select("SELECT * FROM machine_program;")
dbObj = DatabaseObject(result[0])
machPro = MachineProgram(dbObj)
print(machPro)