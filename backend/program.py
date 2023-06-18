from database.handler.databaseHandler import DatabaseHandler

from database.orm.machine.machineProgram import MachineProgram

from datetime import datetime

from database.orm.program.programState import ProgramState

class Program:
    
    def __init__(self) -> None:
        #Active Changing Parameters
        self.programCurrentAmount: int = 0
        self.programRuntime: int = 0
        self.programLaserModulePowerConsumption: int = 0
        
        #Static Parameters
        self.programId: int = None
        self.isProgramRunning: bool = False
        self.programTargetAmount: int = 100
        self.programMachineProgramId: int = None
        self.programProgramDescription: str = ""
        self.programLaserModuleWeardown: int = 0
        self.programCoolantConsumption: int = 0
        self.programTimePerItem: int = 0 
        self.newItems: int = 0
        
        self.machineProgram = None
        
        self.programStartTime: datetime = None
        self.programStopTime: datetime = None
        self.programTimeSinceLastUpdate: datetime = None
        self.lastUpdate: datetime = None
        
    def getProgramStopTime(self) -> datetime:
        return self.programStopTime
    
    def setProgramStopTime(self, stopTime: datetime) -> None:
        self.programStopTime = stopTime
    
    def getIsProgramRunning(self) -> bool:
        return self.isProgramRunning
    
    def setIsProgramRunning(self, bool: bool) -> None:
        self.isProgramRunning = bool
    
    def getProgramId(self) -> int:
        return self.programId
    
    def setProgramId(self, programId: int) -> None:
        self.programId = programId

    def getProgramCurrentAmount(self) -> int:
        return self.programCurrentAmount
    
    def setProgramCurrentAmount(self, programCurrentAmount: int) -> None:
        self.programCurrentAmount = programCurrentAmount
        
    def getProgramRuntime(self) -> int:
        return self.programRuntime
    
    def setProgramRuntime(self, programRuntime: int) -> None:
        self.programRuntime = programRuntime

    def getProgramTargetAmount(self) -> int:
        return self.programTargetAmount
    
    def setProgramTargetAmount(self, programTargetAmount: int) -> None:
        self.programTargetAmount = programTargetAmount
    
    def getProgramMachineProgramId(self) -> int:
        return self.programMachineProgramId
    
    def setProgramMachineProgramId(self, programMachineProgramId: int) -> None:
        self.programMachineProgramId = programMachineProgramId    
    
    def getProgramProgramDescription(self) -> str:
        return self.programProgramDescription
    
    def setProgramProgramDescription(self, programProgramDescription: str) -> None:
        self.programProgramDescription = programProgramDescription
    
    def getProgramLaserModuleWeardown(self) -> int:
        return self.programLaserModuleWeardown
    
    def setProgramLaserModuleWeardown(self, programLaserModuleWeardown: int) -> None:
        self.programLaserModuleWeardown = programLaserModuleWeardown

    def getProgramCoolantConsumption(self) -> int:
        return self.programCoolantConsumption
    
    def setProgramCoolantConsumption(self, programCoolantConsumption: int) -> None:
        self.programCoolantConsumption = programCoolantConsumption

    def getProgramLaserModulePowerConsumption(self) -> int:
        return self.programLaserModulePowerConsumption
        
    def setProgramLaserModulePowerConsumption(self, programLaserModulePowerConsumptio) -> None:
        self.programLaserModulePowerConsumption = programLaserModulePowerConsumptio
        
    def getProgramTimePerItem(self) -> int:
        return self.programTimePerItem

    def setProgramTimePerItem(self, programTimePerItem) -> None:
        self.programTimePerItem = programTimePerItem
        
    def loadProgramState(self, programState: ProgramState) -> None:
        self.machineProgram =  DatabaseHandler.selectMachineProgramById(programState.getID())
        self.loadMachineProgram()
        self.programId = programState.getID()
        self.programTargetAmount = programState.getTargetAmount()
        self.programCurrentAmount = programState.getCurrentAmount()
        self.programRuntime = programState.getRuntime()
        self.lastUpdate = None
        
    def loadMachineProgram(self) -> None:
        self.setIsProgramRunning(False)
        self.setProgramId(self.machineProgram.getID())
        self.setProgramProgramDescription(self.machineProgram.getDescription())
        self.setProgramLaserModuleWeardown(self.machineProgram.getLaserModuleWeardown()*0.01)
        self.setProgramCoolantConsumption(self.machineProgram.getCoolantConsumption()*0.01)
        self.setProgramLaserModulePowerConsumption(self.machineProgram.getLaserModulePowerConsumption())
        self.setProgramTimePerItem(self.machineProgram.getTimePerItem())

    def checkAmount(self) -> bool:
        if self.programCurrentAmount >= self.programTargetAmount:
            return False
        else:
            return True

    def updateProgram(self, newTime: datetime):
        checker: bool = self.checkAmount()
        while checker == True:    
            if(self.isProgramRunning == True and self.programStartTime is not None):
                self.calculateProgramRuntime(newTime)
                #if(self.programCurrentAmount >= self.programTargetAmount):
                #    self.setIsProgramRunning(False)
                self.updateProgramCurrentAmount()
                self.updateProgramLaserModulePowerConsumption()
                return [ self.programLaserModulePowerConsumption,self.programCoolantConsumption, self.newItems, self.isProgramRunning, self.programLaserModuleWeardown]
            if checker == False:
                self.stopProgram(datetime.now())
                # break
        return [ self.programLaserModulePowerConsumption,self.programCoolantConsumption, self.newItems, self.isProgramRunning, self.programLaserModuleWeardown]
        
    def calculateProgramRuntime(self, nowTime: datetime) -> None:
        if(self.lastUpdate == None):
            self.lastUpdate = self.programStartTime
            
        self.programTimeSinceLastUpdate = (nowTime - self.lastUpdate).total_seconds()
        self.programRuntime = self.programRuntime + self.programTimeSinceLastUpdate
        self.lastUpdate = nowTime
        
    def updateProgramCurrentAmount(self) -> None:
        self.newItems = self.programTimeSinceLastUpdate / self.programTimePerItem
        self.programCurrentAmount = self.programCurrentAmount + self.newItems
    
    def updateProgramLaserModulePowerConsumption(self) -> None:
        self.programLaserModulePowerConsumption = self.programLaserModulePowerConsumption + self.programTimeSinceLastUpdate / self.programTimePerItem
    
    def resetProgram(self) -> None:
        self.isProgramRunning = False
        self.loadMachineProgram()

    def setMachineProgram(self, machineProgram: MachineProgram) -> None:
        self.machineProgram = machineProgram
        self.loadMachineProgram()

    def startProgram(self, startTime: datetime) -> None:
        self.isProgramRunning = True
        self.programStartTime = startTime

    def stopProgram(self, stopTime: datetime) -> None:
        self.isProgramRunning = False
        self.programStopTime = stopTime
        
    def getProgramStateSnapshot(self) -> dict:
        parameters = [{"description": "Program Runtime", "value": int(self.getProgramRuntime())},
                           {"description": "Target Amount", "value": int(self.getProgramTargetAmount())},
                           {"description": "Current Amount", "value": int(self.getProgramCurrentAmount())},
                           {"description": "Coolant Consumption per S", "value": self.getProgramCoolantConsumption()},
                           {"description": "Laser Module Wear Down", "value": self.getProgramLaserModuleWeardown()},
                           {"description": "Laser Power Consumption", "value": int(self.getProgramLaserModulePowerConsumption())},
                           {"description": "Time per Item", "value": self.getProgramTimePerItem()},
                           ]
        data = {
            "description": self.getProgramProgramDescription(),
            "parameters": []
        }
        for index, param in enumerate(parameters):
            parameter = {
                "id": index,
                "description": param["description"],
                "value": param["value"]
            }
            data["parameters"].append(parameter)
        return data
        
    def getDict(self) -> dict:
        return {
            "programCurrentAmount":self.programCurrentAmount,
            "programRuntime":self.programRuntime,
            "programLaserModulePowerConsumption":self.programLaserModulePowerConsumption,
            "programId":self.programId,
            "isProgramRunning":self.isProgramRunning,
            "programTargetAmount":self.programTargetAmount,
            "programMachineProgramId":self.programMachineProgramId,
            "programProgramDescription":self.programProgramDescription,
            "programLaserModuleWeardown":self.programLaserModuleWeardown,
            "programCoolantConsumption":self.programCoolantConsumption,
            "programTimePerItem":self.programTimePerItem,
            "newItems":self.newItems,
            "machineProgram":self.machineProgram,
            "programStartTime":self.programStartTime,
            "programTimeSinceLastUpdate":self.programTimeSinceLastUpdate,
            "lastUpdate":self.lastUpdate,
            }
    def getAsProgramState(self) -> ProgramState:
        return ProgramState(0, self.programId, self.programTargetAmount, self.programCurrentAmount, self.programRuntime )