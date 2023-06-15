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
    
    def __init__(self, id: int, name: str, errorState: int, warningState: int, programState: int, machineStartTime: int, machineStopTime: int, machineDownTime: int, allItems: int, energyConsumptionWatt: float, capacityLaserModule: float, coolantLevelMl: float) -> None:
        self.ID: int = id
        self.name: str = name
        self.errorState: int = errorState
        self.warningState: int = warningState
        self.programState: int = programState
        self.machineStartTime: int = machineStartTime
        self.machineStopTime: int = machineStopTime
        self.machineDownTime: int = machineDownTime
        self.allItems: int = allItems
        self.energyConsumptionWatt: float = energyConsumptionWatt
        self.capacityLaserModule: float = capacityLaserModule
        self.coolantLevelMl: float= coolantLevelMl
        

    def getID(self) -> int:
        return self.ID
    
    def getName(self) -> str:
        return self.name
    
    def getErrorState(self) -> int:
        return self.errorState
    
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
        return self.allItems
    
    def getEnergyConsumptionWatt(self) -> int:
        return self.energyConsumptionWatt
    
    def getCapacityLaserModule(self) -> float:
        return self.capacityLaserModule
    
    def getCoolantLevelMl(self) -> float:
        return self.coolantLevelMl
    
    def __str__(self):
        return f"ID: {self.ID}\n" \
               f"Name: {self.name}\n" \
               f"Error state: {self.errorState}\n" \
               f"Warning state: {self.warningState}\n" \
               f"Program state: {self.programState}\n" \
               f"Machine start time: {self.machineStartTime}\n" \
               f"Machine stop time: {self.machineStopTime}\n" \
               f"Machine down time: {self.machineDownTime}\n" \
               f"All items: {self.allItems}\n" \
               f"Energy consumption (Watt): {self.energyConsumptionWatt}\n" \
               f"Capacity of laser module: {self.capacityLaserModule}\n" \
               f"Coolant level (mL): {self.coolantLevelMl}"
    
    def getJson(self):
        return {
            "id": self.ID,
            "name": self.name,
            "errorState": self.errorState,
            "warningState": self.warningState,  # Corrected typo here
            "programState": self.programState,
            "machineStartTime": self.machineStartTime,
            "machineStopTime": self.machineStopTime,
            "machineDownTime": self.machineDownTime,
            "allItems": self.allItems,
            "energyConsumptionWatt": self.energyConsumptionWatt,
            "capacityLaserModule": self.capacityLaserModule,
            "coolantLevelMl": self.coolantLevelMl
        }

        