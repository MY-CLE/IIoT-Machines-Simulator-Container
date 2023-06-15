from database.handler.databaseHandler import DatabaseHandler
from database.orm.machine.machineProgram import MachineProgram
from database.orm.program.programState import ProgramState
from database.orm.databaseObject import DatabaseObject
from mode import Mode

#extends class mode
#retrieves the triangle mode specific parameters out of the database
class Triangle(Mode):
     
   def __init__(self) -> None:
      program: MachineProgram = DatabaseHandler.selectMachineProgram('Triangle')
      programState: ProgramState = DatabaseHandler.selectProgramState(2)
      super().__init__(program.getPowerComsumptionKwH(), program.getLaserModuleWeardown(), program.getTimePerItem(), programState.getTargetAmount(), program.getDescription()) 
      
   def getProgramId(self) -> int:
         return self.program.getID()