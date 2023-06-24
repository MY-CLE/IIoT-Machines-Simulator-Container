from database.orm.databaseObject import DatabaseObject
from datetime import datetime

class MachineState(object):


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
    
    def getLastEdited(self) -> datetime:
        return self.lastEdited
    
    def getMachineProtocol(self) -> int:
        return self.machineProtocol
        
    def getName(self) -> str:
        return self.machineStateName
    
    def getErrorState(self) -> int:
        return self.errorState
    
    def getWarningState(self) -> int:
        return self.warningState
    
    def getProgramState(self) -> int:
        return self.programState
    
    def getMachineStartTime(self) -> datetime:
        return self.machineStartTime
    
    def getMachineStopTime(self) -> datetime:
        return self.machineStopTime
    
    def getMachineDownTime(self) -> int:
        return self.machineDownTime
    
    def getMachineRuntime(self) -> int:
        return self.machineRunTime
    
    def getAllItems(self) -> int:
        return self.totalItems
    
    def getEnergyConsumptionWatt(self) -> int:
        return self.energyConsumptionWatt
    
    def getCapacityLaserModule(self) -> float:
        return self.capacityLasermodule
    
    def getCoolantLevelMl(self) -> float:
        return self.coolantLevel
    
    def __str__(self):
        return f"Machine State ID: {self.machineStateID}\n" \
           f"Last Edited: {self.lastEdited}\n" \
           f"Machine Protocol: {self.machineProtocol}\n" \
           f"Machine State Name: {self.machineStateName}\n" \
           f"Error State: {self.errorState}\n" \
           f"Warning State: {self.warningState}\n" \
           f"Program State: {self.programState}\n" \
           f"Machine Start Time: {self.machineStartTime}\n" \
           f"Machine Stop Time: {self.machineStopTime}\n" \
           f"Machine Down Time: {self.machineDownTime}\n" \
           f"Machine Run Time: {self.machineRunTime}\n" \
           f"Total Items: {self.totalItems}\n" \
           f"Energy Consumption (Watt): {self.energyConsumptionWatt}\n" \
           f"Capacity of Laser Module: {self.capacityLasermodule}\n" \
           f"Coolant Level (mL): {self.coolantLevel}"

    
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
    
    def __eq__(self, other):
        if other != None:
            return (
                self.machineStateID == other.machineStateID
                and self.machineProtocol == other.machineProtocol
                and self.machineStateName == other.machineStateName
                and self.errorState == other.errorState
                and self.warningState == other.warningState
                and self.programState == other.programState
                and self.totalItems == other.totalItems
                and self.energyConsumptionWatt == other.energyConsumptionWatt
                and self.capacityLasermodule == other.capacityLasermodule
                and self.coolantLevel == other.coolantLevel
            )
        return False

        