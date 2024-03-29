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
        self.programTimePerItem: int = 1 
        self.newItems: int = 0
        
        self.machineProgram = None
        
        #Times
        self.programStartTime: datetime = None
        self.programStopTime: datetime = None
        self.programTimeSinceLastUpdate: datetime = None
        self.lastUpdate: datetime = None
        self.additionalTime: int = 0
        
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
        self.additionalTime = programRuntime - self.programRuntime
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
        self.setProgramRuntime(0)
        self.setProgramId(self.machineProgram.getID())
        self.setProgramProgramDescription(self.machineProgram.getDescription())
        self.setProgramLaserModuleWeardown(round(self.machineProgram.getLaserModuleWeardown()*0.0001, 4))
        self.setProgramCoolantConsumption(self.machineProgram.getCoolantConsumption()*0.001)
        self.setProgramLaserModulePowerConsumption(self.machineProgram.getLaserModulePowerConsumption())
        self.setProgramTimePerItem(self.machineProgram.getTimePerItem())


    def updateProgram(self, newTime: datetime):
        
        if(self.isProgramRunning and self.programStartTime is not None):
            self.calculateProgramRuntime(newTime)
            #if(self.programCurrentAmount >= self.programTargetAmount):
            #    self.setIsProgramRunning(False)
            self.updateProgramCurrentAmount()
            self.updateProgramLaserModulePowerConsumption()
            if (self.programCurrentAmount > self.programTargetAmount):    
                self.programCurrentAmount = self.programTargetAmount
                self.stopProgram(datetime.now())
            
        passAdditionalTime = self.additionalTime  
        self.additionalTime = 0
        return [ self.programLaserModulePowerConsumption,self.programCoolantConsumption, self.newItems, self.isProgramRunning, self.programLaserModuleWeardown, passAdditionalTime]
        
    def calculateProgramRuntime(self, nowTime: datetime) -> None:
        if(self.lastUpdate == None):
            self.lastUpdate = self.programStartTime
            
        if(self.additionalTime != 0):
            self.programTimeSinceLastUpdate = self.additionalTime
            
        else:
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
        if self.machineProgram is not None:
            self.loadMachineProgram()
        else:
            self.startProgram(0)
        
    def resetToDefaultState(self) -> None:
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
        self.programTimePerItem: int = 1 
        self.newItems: int = 0
        
        self.machineProgram = None
        
        #Times
        self.programStartTime: datetime = None
        self.programStopTime: datetime = None
        self.programTimeSinceLastUpdate: datetime = None
        self.lastUpdate: datetime = None
        self.additionalTime: int = 0

    def setMachineProgram(self, machineProgram: MachineProgram) -> None:
        self.machineProgram = machineProgram
        self.loadMachineProgram()

    def startProgram(self, startTime: datetime) -> None:
        self.isProgramRunning = True
        self.programStartTime = startTime
        self.programTimeSincelastUpdate = None

    def stopProgram(self, stopTime: datetime) -> None:
        self.isProgramRunning = False
        self.programStopTime = stopTime
        self.lastUpdate = None
        
    def checkMachineRuntimeValue(self, machineRuntime: int) -> None:
        if self.programRuntime > machineRuntime:
            self.programRuntime = machineRuntime 
        
    def getProgramStateSnapshot(self) -> dict:
        parameters = [{"description": "Program Runtime (s)", "value": int(self.getProgramRuntime()), "isAdminParameter": False, "maxValue": 65535},
                           {"description": "Target Amount", "value": int(self.getProgramTargetAmount()), "isAdminParameter": False, "maxValue": 65535},
                           {"description": "Current Amount", "value": int(self.getProgramCurrentAmount()), "isAdminParameter": False, "maxValue": 65535},
                           {"description": "Coolant Consumption (% / s)", "value": self.getProgramCoolantConsumption(), "isAdminParameter": True, "maxValue": 65535},
                           {"description": "Laser Module Weardown (% / s)", "value": self.getProgramLaserModuleWeardown(), "isAdminParameter": True, "maxValue": 65535},
                           {"description": "Laser Power Consumption (W)", "value": int(self.getProgramLaserModulePowerConsumption()), "isAdminParameter": True, "maxValue": 65535},
                           {"description": "Time per Item (s)", "value": self.getProgramTimePerItem(), "isAdminParameter": True, "maxValue": 65535},
                           ]
        data = {
            "description": self.getProgramProgramDescription(),
            "parameters": []
        }
        for index, param in enumerate(parameters):
            parameter = {
                "id": index,
                "description": param["description"],
                "value": param["value"],
                "isAdminParameter": param["isAdminParameter"],
                "maxValue": param["maxValue"]
            }
            data["parameters"].append(parameter)
        return data
        
    def toDict(self) -> dict:
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