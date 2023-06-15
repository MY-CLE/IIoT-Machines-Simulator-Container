from database.orm.databaseObject import DatabaseObject

class MachineProgram(object):
    
    def __init__(self, databaseObject: DatabaseObject) -> None:
        self.ID: int = databaseObject.getResultRow()[0]
        self.description: str = databaseObject.getResultRow()[1]
        self.laserModuleWeardown: int = databaseObject.getResultRow()[2]
        self.coolantConsumptionMl: int = databaseObject.getResultRow()[3]
        self.powerConsumptionKwH: int = databaseObject.getResultRow()[4]
        self.timePerItem: int = databaseObject.getResultRow()[5]
    
    def getID(self) -> int:
        return self.ID
    
    def getDescription(self) -> str:
        return self.description
    
    def getLaserModuleWeardown(self) -> int:
        return self.laserModuleWeardown
    
    def getPowerComsumptionKwH(self) -> int:
        return self.powerConsumptionKwH
    

    def getCoolantConsumptionMl(self) -> int:
        return self.coolantConsumptionMl
    
    def getTimePerItem(self) -> int:
        return self.timePerItem
    
    def __str__(self) -> str:
        return f"stateID: {self.ID}, ID: {self.description}, targetAmount: {self.laserModuleWeardown}, currentAmount: {self.coolantConsumptionMl}, runtime: {self.timePerItem }"
        
