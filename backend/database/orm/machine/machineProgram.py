from database.orm.databaseObject import DatabaseObject

class MachineProgram(object):
    
    #def __init__(self, databaseObject: DatabaseObject) -> None:
    #    self.ID: int = databaseObject.getResultRow()[0]
    #    self.description: str = databaseObject.getResultRow()[1]
    #    self.laserModuleWeardown: int = databaseObject.getResultRow()[2]
    #    self.coolantConsumptionMl: int = databaseObject.getResultRow()[3]
    #    self.powerConsumptionKwH: int = databaseObject.getResultRow()[4]
    #    self.timePerItem: int = databaseObject.getResultRow()[5]
    
    def __init__(self, ID: int, description: str, laserModuleWeardown: int, coolantConsumptionMl: int, powerConsumptionLaserModule  , timePerItem: int) -> None:
        self.ID: int = ID
        self.description: str = description
        self.laserModuleWeardown: int = laserModuleWeardown
        self.coolantConsumption: int = coolantConsumptionMl
        self.powerConsumptionLaserModule: int = powerConsumptionLaserModule
        self.timePerItem: int = timePerItem
        
    def getID(self) -> int:
        return self.ID
    
    def getDescription(self) -> str:
        return self.description
    
    def getLaserModuleWeardown(self) -> int:
        return self.laserModuleWeardown
    
    def getLaserModulePowerConsumption(self) -> int:
        return self.powerConsumptionLaserModule
    

    def getCoolantConsumption(self) -> int:
        return self.coolantConsumption
    
    def getTimePerItem(self) -> int:
        return self.timePerItem
    
    def __str__(self) -> str:
        return f"stateID: {self.ID}, ID: {self.description}, targetAmount: {self.laserModuleWeardown}, currentAmount: {self.coolantConsumptionMl}, runtime: {self.timePerItem }"
        
    def toJSON(self) -> dict:
        return {
            "id": self.ID,
            "description": self.description,
            "laserModuleWeardown": self.laserModuleWeardown,
            "coolantConsumption": self.coolantConsumption,
            "powerConsumptionLaserModule": self.powerConsumptionLaserModule,
            "timePerItem": self.timePerItem
        }
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return (
            self.ID == other.ID
            and self.description == other.description
            and self.laserModuleWeardown == other.laserModuleWeardown
            and self.coolantConsumption == other.coolantConsumption
            and self.powerConsumptionLaserModule == other.powerConsumptionLaserModule
            and self.timePerItem == other.timePerItem
        )
        return False
