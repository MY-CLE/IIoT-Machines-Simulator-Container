from database.orm.databaseObject import DatabaseObject
from datetime import datetime
class ProgramState(object):

    def __init__(self, databaseObject: DatabaseObject) -> None:
        self.stateID: int  = databaseObject.getResultRow()[0]
        self.ID: int  = databaseObject.getResultRow()[1]
        self.targetAmount: int = databaseObject.getResultRow()[2]
        self.currentAmount: int = databaseObject.getResultRow()[3]
        self.runtime:int = databaseObject.getResultRow()[4]

    def getStateID(self) -> int:
        return self.stateID
    
    def getID(self) -> int:
        return self.ID
    
    def getTargetAmount(self) -> int:
        return self.targetAmount
    
    def getCurrentAmount(self) -> int:
        return self.currentAmount
    
    def getRuntime(self) -> int:
        return self.runtime
    
    def __str__(self):
        return f"MyClass(stateID: {self.stateID}, ID: {self.ID}, targetAmount: {self.targetAmount}, currentAmount: {self.currentAmount}, runtime: {self.runtime})"