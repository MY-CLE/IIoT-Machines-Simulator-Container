import json

from database.orm.machine.machineProgram import MachineProgram

from datetime import datetime

class Program:
    
    def __init__(self) -> None:
        #Active Changing Parameters
        self.programCurrentAmount: int = 0
        self.programRuntime: int = 0
        self.programLaserModulePowerConsumption: int = 0
        
        #Static Parameters
        self.programId: int = None
        self.isProgramRunning: bool = False
        self.programTargetAmount: int = None
        self.programMachineProgramId: int = None
        self.programProgramDescription: str = None
        self.programLaserModuleWeardown: int = None
        self.programCoolantConsumption: int = None
        self.programTimePerItem: int = None
        
        self.programStartTime: datetime = None
        self.programTimeSinceLastUpdate: datetime = None
        
    
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
        self.programCurrentAmount = programTargetAmount
    
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
        
    def changeProgram(self, machineProgram: MachineProgram) -> None:
        self.setIsProgramRunning(False)
        self.setProgramId(machineProgram.getID())
        self.setProgramProgramDescription(machineProgram.getDescription())
        self.setProgramLaserModuleWeardown(machineProgram.getLaserModuleWeardown())
        self.setProgramCoolantConsumption(machineProgram.getCoolantConsumption())
        self.setProgramLaserModulePowerConsumption(machineProgram.getLaserModulePowerConsumption())
        self.setProgramTimePerItem(machineProgram.getTimePerItem())
        
    def updateProgram(self, newTime: datetime):
        if(self.isProgramRunning == True):
            self.calculateProgramRuntime(newTime)
            if(self.programCurrentAmount >= self.programTargetAmount):
                self.setIsProgramRunning(False)
            self.updateProgramCurrentAmount()
            self.updateProgramLaserModulePowerConsumption()

    def calculateProgramRuntime(self, nowTime: datetime) -> None:
        self.programTimeSinceLastUpdate = nowTime.total_seconds() - self.programStartTime.total_seconds()
        self.programRuntime = self.programRuntime + self.programTimeSinceLastUpdate
        
    def updateProgramCurrentAmount(self) -> None:
        self.programCurrentAmount = self.programCurrentAmount + self.programTimeSinceLastUpdate / self.programTimePerItem
    
    def updateProgramLaserModulePowerConsumption(self) -> None:
        self.programLaserModulePowerConsumption = self.programLaserModulePowerConsumption + self.programTimeSinceLastUpdate / self.programTimePerItem
    

    def getJson(self) -> str:
        return json.dumps(self.__dict__)