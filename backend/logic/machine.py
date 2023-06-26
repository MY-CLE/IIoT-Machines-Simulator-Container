from datetime import datetime
import logging
from venv import logger
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
        
        #Errors & Warnings
        self.activeErrors: list = []
        self.activeWarnings: list = []

        #Active
        self.isProgramRunning: bool = False
        self.isMachineRunning: bool = False
        
        #Times
        self.machineStartTime: datetime = None
        self.machineStopTime: datetime = None
        self.machineIdleTime: int= 0
        self.machineRuntime: int = 0
        self.timeSinceLastUpdate: int = None
        self.lastUpdate: datetime = None
        self.additionalTime: int = 0
        
        #Parameter
        self.totalItems: int= 0
        self.totalEnergyConsumption: int = 0
        self.capacityLaserModule: int = 100
        self.coolantLevel: int = 100

    def calculateTimes(self, nowTime:datetime):
        if(self.lastUpdate == None):
            self.lastUpdate = self.machineStartTime
        if(self.additionalTime != 0):
            if(self.additionalTime < 0):
                self.additionalTime = 0
            self.timeSinceLastUpdate = self.additionalTime
            self.additionalTime = 0
        else:
            self.timeSinceLastUpdate = (nowTime - self.lastUpdate).total_seconds()
            self.machineRuntime += self.timeSinceLastUpdate
        self.lastUpdate = nowTime
    
    def calculateIdleTime(self, nowTime: datetime) -> None:
        self.lastUpdate = nowTime
        if self.isProgramRunning:
            self.machineIdleTime = 0
        else:
            machineStopTime = self.getMachineStopTime()
            if machineStopTime is not None:
                self.machineIdleTime += (nowTime - machineStopTime).total_seconds()
            self.setMachineStopTime(nowTime)

    def startMachine(self, startTime: datetime) -> None:
        self.machineStartTime = startTime
        self.machineStopTime = startTime
        self.isMachineRunning = True
        self.lastUpdate = None
    
    def stopMachine(self, stopTime: datetime) -> None:
        self.machineStopTime = stopTime
        self.isMachineRunning = False

    def resetMachine(self):
        self.isProgramRunning = False
        self.setMachineIdleTime(0)
        self.setMachineRuntime(0)
        self.setTotalItems(0)
        self.setCapacityLaserModule(100)
        self.setTotalEnegeryConsumption(0)
        self.setCoolantLevel(100)
        self.setMachineStartTime(datetime.now())
        self.lastUpdate = None
        
    def updateMachineErrors(self, newErrors: list, newWarnings: list):
        self.activeErrors = newErrors
        self.activeWarnings = newWarnings
        logging.info("Errors: " + str(self.activeErrors))
        logging.info("Warnings: " + str(self.activeWarnings))
        
    def updateMachine(self, nowTime: datetime, powerConsumptionPerS: int, coolantConsumptionPerS: int, newItems: int, isProgramRunning: bool, laserModuleWeardown: float, programAdditionalTime: int):
        self.isProgramRunning = isProgramRunning
        self.additionalTime += programAdditionalTime
        self.machineRuntime += programAdditionalTime
        if(self.machineStartTime != None):
            self.calculateTimes(nowTime)
            self.totalItems =  self.totalItems + newItems
            self.totalEnergyConsumption = self.totalEnergyConsumption + powerConsumptionPerS * self.timeSinceLastUpdate
            self.coolantLevel = self.coolantLevel - coolantConsumptionPerS * self.timeSinceLastUpdate
            self.capacityLaserModule = self.capacityLaserModule - laserModuleWeardown*self.timeSinceLastUpdate
        return self.machineRuntime

    def loadMachineState(self, machineState: MachineState):
        self.isProgramRunning =False

        self.machineStateId = machineState.getId()
        self.machineStateName = machineState.getName()
        self.lastEdited = machineState.getLastEdited()

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
        self.totalEnergyConsumption = machineState.getEnergyConsumptionWatt()
        self.capacityLaserModule = machineState.getCapacityLaserModule()
        
    def toDict(self):
        return {
            "machineStateId": self.machineStateId,
            "machineStateName": self.machineStateName,
            "machineProtocolId": self.machineProtocolId,
            "lastEdited": self.lastEdited,
            "errorStateId": self.errorStateId,
            "warningStateId": self.warningStateId,
            "programStateId": self.programStateId,
            "machineStartTime": self.machineStartTime,
            "machineStopTime": self.machineStopTime,
            "machineIdleTime": self.machineIdleTime,
            "machineRuntime": self.machineRuntime,
            "totalItems": self.totalItems,
            "totalEnergyConsumption": self.totalEnergyConsumption,
            "capacityLaserModule": self.capacityLaserModule,
            "coolantLevel": self.coolantLevel
            }
            
    def getMachineStateSnapshot(self) -> dict:
        parameters = [{"id": "1","description": "Runtime (s)", "value": int(self.machineRuntime),"isAdminParameter": False, "maxValue": 65535},
                {"id":"2", "description": "Idle Time (s)", "value": int(self.machineIdleTime),"isAdminParameter": False, "maxValue": 65535},
                {"id":"3","description": "Coolant Level (%)", "value": int(self.coolantLevel), "isAdminParameter": True, "maxValue": 100},
                {"id":"4", "description": "Power Consumption (Wh)", "value": int(self.totalEnergyConsumption), "isAdminParameter": False, "maxValue": 65535},
                {"id":"5", "description": "Capacity Laser Module (%)", "value": int(self.capacityLaserModule), "isAdminParameter": True, "maxValue": 100},
                {"id":"6", "description": "Total Items", "value": int(self.totalItems), "isAdminParameter": True, "maxValue": 65535}]
        
        errors = []
        for index, error in enumerate(self.activeErrors):
            tempError = {
                "id": str(index),
                "name": error
            }
            errors.append(tempError)
        
        warnings = []
        for index, warning in enumerate(self.activeWarnings):
            tempWarning = {
                "id": str(index),
                "name": warning
            }
            warnings.append(tempWarning)
            
        data = {
            "isProgramRunning": self.isProgramRunning,
            "machineStateId": self.machineStateId,
            "machineStateName": self.machineStateName,
            "machineProtocolId": self.machineProtocolId,
            "lastEdited": self.lastEdited,
            "parameters": parameters,
            "errorState": {
               "errors": errors,
               "warnings": warnings,
               }
        }
        logging.info("MachineStateSnapshot: " + str(data))
        return data 
    
    def prepareForDB(self, lastEdited, machineStateName, machineProtocolId, programStateId):
        self.lastEdited = lastEdited
        self.machineStateName = machineStateName
        self.machineProtocolId = machineProtocolId
        self.programStateId = programStateId
        
        if(len(self.activeErrors) != 0):
            self.errorStateId = self.activeErrors[0]["id"]
        else:
            self.errorStateId = 0
        
        if(len(self.activeWarnings) != 0):
            self.warningStateId = self.activeWarnings[0]["id"]
        else:
            self.warningStateId = 0
    
    def getAsMachineState(self) -> MachineState:
        return MachineState(self.machineStateId, self.lastEdited, self.machineProtocolId, self.machineStateName, self.errorStateId, self.warningStateId, self.programStateId, self.machineStartTime, self.machineStopTime, self.machineIdleTime, self.machineRuntime, self.totalItems, self.totalEnergyConsumption, self.capacityLaserModule, self.coolantLevel)

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
        self.additionalTime = machineRuntime - self.machineRuntime
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
        
    def getActiveErrors(self) -> list:
        return self.activeErrors
    
    def setActiveErrors(self, activeErrors: list) -> None:
        self.activeErrors = activeErrors
    
    def getActiveWarnings(self) -> list:
        return self.activeWarnings
    
    def setActiveWarnings(self, activeWarnings: list) -> None:
        self.activeWarnings = activeWarnings
        
    def setIsProgramRunning(self, isProgramRunning: bool) -> None:
        self.isProgramRunning = isProgramRunning


