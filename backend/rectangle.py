from database.handler.databaseHandler import DatabaseHandler
from database.orm.machine.machineProgram import MachineProgram
from database.orm.program.programState import ProgramState
from database.orm.databaseObject import DatabaseObject
from mode import Mode

#extends class mode
#retrieves the rectangle mode specific parameters out of the database
class Rectangle(Mode):
     
     def __init__(self) -> None:
          self.program: MachineProgram = DatabaseHandler.selectMachineProgram('Rectangle')
          self.programState: ProgramState = DatabaseHandler.selectProgramState(1) 
          super().__init__(self.program.getPowerComsumptionKwH(), self.program.getLaserModuleWeardown(), self.program.getTimePerItem(), self.programState.getTargetAmount())
          
     def getProgramId(self) -> int:
         return self.program.getID()