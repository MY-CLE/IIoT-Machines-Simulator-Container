from orm.databaseObject import DatabaseObject

class MachineProgram(object):
    
    def __init__(self, databaseObject: DatabaseObject) -> None:
        self.ID: int = databaseObject.getResultRow()[0]
        self.description: str = databaseObject.getResultRow()[1]
        self.laserPowerConsumptionWatt: int = databaseObject.getResultRow()[2]
        self.coolantConsumptionMl: float = databaseObject.getResultRow()[3]
        self.timePerItem: float = databaseObject.getResultRow()[4]
    
    def getID(self) -> int:
        return self.ID
    
    def getDescription(self) -> str:
        return self.description
    
    def getLaserPowerConsumptionWatt(self) -> int:
        return self.laserPowerConsumptionWatt
    
    def getCoolantConsumptionMl(self) -> float:
        return self.coolantConsumptionMl
    
    def getTimePerItem(self) -> float:
        return self.timePerItem
    
    def __str__(self) -> str:
        return f"stateID: {self.ID}, ID: {self.description}, targetAmount: {self.laserPowerConsumptionWatt}, currentAmount: {self.coolantConsumptionMl}, runtime: {self.timePerItem }"
        
