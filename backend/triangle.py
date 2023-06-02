from database.handler.databaseHandler import DatabaseHandler
from database.orm.machine.machineProgram import MachineProgram
from database.orm.program.programState import ProgramState
from database.orm.databaseObject import DatabaseObject
from mode import Mode

class Triangle(Mode):
     
     def __init__(self) -> None:
        program: MachineProgram = DatabaseHandler.selectMachineProgram('Rectangle')
        programState: ProgramState = DatabaseHandler.selectProgramState(2)
        super().__init__(program.getPowerComsumptionKwH(), program.getLaserModuleWeardown(), program.getTimePerItem(), programState.getTargetAmount())
        