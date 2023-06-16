from datetime import datetime
from database.orm.machine.machineState import MachineState
class Machine():
    
    def __init__(self):
        #When stored/loaded in database
        self.machineStateId: int = None
        self.lastEdited: datetime = None
        self.machineStateName: str = None
        
        self.machineProtocolId: int = None
        self.errorStateId: int = None
        self.warningStateId: int = None
        self.programStateId: int = None
        
        #Active
        self.isProgramRunning: bool = False
        
        #Times
        self.machineStartTime: datetime = None
        self.machineStopTime: datetime = None
        self.machineIdleTime: int= 0
        self.machineRuntime: int = 0
        self.timeSinceLastUpdate: int = None
        
        #Parameter
        self.totalItems: int= 0
        self.totalEnergyConsumption: int = 0
        self.capacityLaserModule: int = 0
        self.coolantLevel: int = 0
        
    def calculateTimes(self, nowTime:datetime):
        self.timeSinceLastUpdate = nowTime.total_seconds() - self.machineStartTime.total_seconds()
        self.machineRuntime += self.timeSinceLastUpdate
        if not self.isProgramRunning:
            self.machineIdleTime = self.machineIdleTime + self.timeSinceLastUpdate

    def resetMachine(self):
        self.isProgramRunning = False
        self.setMachineRuntime(0)
        self.setTotalItems(0)
        self.setCapacityLaserModule(0)
        self.setCoolantLevel(100)
        self.setMachineStartTime(datetime.now())
        
    def updateMachine(self, nowTime: datetime, powerConsumptionPerS: int, coolantConsumptionPerS: int, newItems: int ):
        self.calculateTimes(nowTime)
        self.totalItems =  self.totalItems + newItems
        self.totalEnergyConsumption = self.totalEnergyConsumption + powerConsumptionPerS*self.timeSinceLastUpdate
        self.coolantLevel = self.coolantLevel + coolantConsumptionPerS*self.timeSinceLastUpdate

    def setMachine(self, machineState: MachineState):
        self.isProgramRunning(False)

        self.machineStateId = machineState.getID()
        self.machineStateName = machineState.getName()
        self.lastEdited - machineState.getLastEdited()

        self.errorStateId = machineState.getErrorState()
        self.warningStateId = machineState.getWarningState()
        self.programStateId = machineState.getProgramState()
        self.machineProtocolId = machineState.getMachineProtocol()

        self.machineStartTime = machineState.getMachineStartTime()
        self.machineStopTime = machineState.getMachineStopTime()
        self.machineIdleTime = machineState.getMachineDownTime()
        self.machineRuntime = machineState.getMachineRuntime()

        self.totalItems = machineState.getAllItems()
        self.coolantLevel = machineState.getCoolantLevelMl()
        self.totalEnergyConsumption = machineState.energyConsumptionWatt()
        self.capacityLaserModule = machineState.getCapacityLaserModule()

    def getJson(self) -> str:
        return json.dumps(self.__dict__)

    def getMachineStateId(self) -> int:
        return self.machineStateId
    
    def setMachineStateId(self, machineStateId: int) -> None:
        self.machineStateId = machineStateId

    def getLastEditted(self):
        return self.lastEdited

    def setLastEditted(self, lastEditted: datetime) -> None:
        self.lastEdited = lastEditted
    
    def getMachineStateName(self):
        return self.machineStateName
    
    def setMachineStateName(self, machineStateName: str) -> None:
        self.machineStateName = machineStateName
    
    def getMachineProtocolId(self):
        return self.machineProtocolId
    
    def setMachineProtocolId(self, machineProtocolId: int) -> None:
        self.machineProtocolId = machineProtocolId
        
    def getErrorStateId(self) -> int:
        return self.errorStateId
    
    def setErrorStateId(self, errorStateId: int) -> None:
        self.errorStateId = errorStateId

    def getWarningStateId(self) -> int:
        return self.warningStateId
    
    def setWarningStateId(self, warningStateId: int) -> None:
        self.warningStateId = warningStateId

    def getProgramStateId(self) -> int:
        return self.programStateId
    
    def setProgramStateId(self, programStateId: int) -> int:
        self.programStateId = programStateId
        
    def getMachineStartTime(self) -> datetime:
        return self.machineStartTime
    
    def setMachineStartTime(self, machineStartTime: datetime) -> None:
        self.machineStartTime = machineStartTime

    def getMachineStopTime(self) -> datetime:
        return self.machineStopTime
    
    def setMachineStopTime(self, machineStopTime: datetime) -> None:
        self.machineStopTime = machineStopTime

    def getMachineIdleTime(self) -> int:
        return self.machineIdleTime
    
    def setMachineIdleTime(self, machineIdleTime: int) -> None:
        self.machineIdleTime = machineIdleTime

    def getMachineRuntime(self) -> int:
        return self.machineRuntime
    
    def setMachineRuntime(self, machineRuntime: int) -> None:
        self.machineRuntime = machineRuntime

    def getTotalItems(self) -> int:
        return self.totalItems
    
    def setTotalItems(self, totalItems: int) -> None:
        self.totalItems = totalItems

    def getTotalEnegeryConsumption(self) -> int:
        return self.totalEnergyConsumption
    
    def setTotalEnegeryConsumption(self, totalEnergyConsumption: int) -> None:
        self.totalEnergyConsumption = totalEnergyConsumption
        
    def getCapacityLaserModule(self) -> int:
        return self.capacityLaserModule
    
    def setCapacityLaserModule(self, capacityLaserModule) -> None:
        self.capacityLaserModule = capacityLaserModule

    def getCoolantLevel(self) -> int:
        return self.coolantLevel
    
    def setCoolantLevel(self, coolantLevel: int) -> None:
        self.coolantLevel = coolantLevel