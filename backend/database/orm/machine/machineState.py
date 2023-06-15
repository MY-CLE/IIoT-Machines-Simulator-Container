from database.orm.databaseObject import DatabaseObject
from datetime import datetime

class MachineState(object):

    #def __init__(self, databaseObject: DatabaseObject) -> None:
    #    self.ID: int = databaseObject.getResultRow()[0]
    #    self.name: str = databaseObject.getResultRow()[1]
    #    self.errorState: int = databaseObject.getResultRow()[2]
    #    self.warningState: int = databaseObject.getResultRow()[3]
    #    self.programState: int = databaseObject.getResultRow()[4]
    #    self.machineStartTime: int = databaseObject.getResultRow()[5]
    #    self.machineStopTime: int = databaseObject.getResultRow()[6]
    #    self.machineDownTime: int = databaseObject.getResultRow()[7]
    #    self.allItems: int = databaseObject.getResultRow()[8]
    #    self.energyConsumptionWatt: int = databaseObject.getResultRow()[9]
    #    self.capacityLaserModule: float = databaseObject.getResultRow()[10]
    #    self.coolantLevelMl: float = databaseObject.getResultRow()[11]
    
    from datetime import datetime
    
    def __init__(self, machineStateID: int, lastEdited: datetime, machineProtocol: int, machineStateName: str, errorState: int, warningState: int, programState: int, 
                 machineStartTime: datetime, machineStopTime: datetime, machineDownTime: int, machineRunTime: int, totalItems: int, energyConsumptionWatt: int, capacityLasermodule: int, coolantLevel: int) -> None:
        self.machineStateID: int = machineStateID
        self.lastEdited: datetime = lastEdited
        self.machineProtocol: int = machineProtocol
        self.machineStateName: str = machineStateName
        self.errorState: int = errorState
        self.warningState: int = warningState
        self.programState: int = programState
        self.machineStartTime: datetime = machineStartTime
        self.machineStopTime: datetime = machineStopTime
        self.machineDownTime: int = machineDownTime
        self.machineRunTime: int = machineRunTime
        self.totalItems: int = totalItems
        self.energyConsumptionWatt: int = energyConsumptionWatt
        self.capacityLasermodule: int = capacityLasermodule
        self.coolantLevel: int = coolantLevel

        

    def getID(self) -> int:
        return self.machineStateID
    
    def getName(self) -> str:
        return self.machineStateName
    
    def getErrorState(self) -> int:
        return self.erroState
    
    def getWarningState(self) -> int:
        return self.warningState
    
    def getProgramState(self) -> int:
        return self.programState
    
    def getMachineStartTime(self) -> int:
        return self.machineStartTime
    
    def getMachineStopTime(self) -> int:
        return self.machineStopTime
    
    def getMachineDownTime(self) -> int:
        return self.machineDownTime
    
    def getAllItems(self) -> int:
        return self.totalItems
    
    def getEnergyConsumptionWatt(self) -> int:
        return self.energyConsumptionWatt
    
    def getCapacityLaserModule(self) -> float:
        return self.capacityLasermodule
    
    def getCoolantLevelMl(self) -> float:
        return self.coolantLevel
    
    def __str__(self):
        return f"ID: {self.ID}\n" \
               f"Name: {self.name}\n" \
               f"Error state: {self.errorState}\n" \
               f"Warning state: {self.warningState}\n" \
               f"Program state: {self.programState}\n" \
               f"Machine start time: {self.machineStartTime}\n" \
               f"Machine stop time: {self.machineStopTime}\n" \
               f"Machine down time: {self.machineDownTime}\n" \
               f"All items: {self.totalItems}\n" \
               f"Energy consumption (Watt): {self.energyConsumptionWatt}\n" \
               f"Capacity of laser module: {self.capacityLasermodule}\n" \
               f"Coolant level (mL): {self.coolantLevel}"
    
    def getJson(self):
        return {
            "id": self.machineStateID,
            "name": self.machineStateName,
            "errorState": self.errorState,
            "warningState": self.warningState,  # Corrected typo here
            "programState": self.programState,
            "machineStartTime": self.machineStartTime,
            "machineStopTime": self.machineStopTime,
            "machineDownTime": self.machineDownTime,
            "allItems": self.totalItems,
            "energyConsumptionWatt": self.energyConsumptionWatt,
            "capacityLaserModule": self.capacityLasermodule,
            "coolantLevelMl": self.coolantLevel
        }

        