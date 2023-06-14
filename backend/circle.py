from database.handler.databaseHandler import DatabaseHandler
from database.orm.machine.machineProgram import MachineProgram
from database.orm.program.programState import ProgramState
from database.orm.databaseObject import DatabaseObject
from mode import Mode

#extends class mode
#retrieves the circle mode specific parameters out of the database
class Circle(Mode):

    def __init__(self) -> None:
        program: MachineProgram = DatabaseHandler.selectMachineProgram('Circle')
        programState: ProgramState = DatabaseHandler.selectProgramState(3)
        super().__init__(program.getPowerComsumptionKwH(), program.getLaserModuleWeardown(), program.getTimePerItem(), programState.getTargetAmount(), program.getDescription())
