from database.handler.databaseHandler import DatabaseHandler
from database.orm.machine.machineProgram import MachineProgram
from database.orm.program.programState import ProgramState
from database.orm.databaseObject import DatabaseObject
from mode import Mode

#extends class mode
#retrieves the circle mode specific parameters out of the database
class Circle(Mode):

    def __init__(self) -> None:
        self.program: MachineProgram = DatabaseHandler.selectMachineProgram('Circle')
        self.programState: ProgramState = DatabaseHandler.selectProgramState(3)
        super().__init__(self.program.getPowerComsumptionKwH(), self.program.getLaserModuleWeardown(), self.program.getTimePerItem(), self.programState.getTargetAmount())        

    def getProgramId(self) -> int:
         return self.program.getID()
