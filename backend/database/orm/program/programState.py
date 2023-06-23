from database.orm.databaseObject import DatabaseObject
from datetime import datetime
class ProgramState(object):

    def __init__(self, stateId, id, targetAmount, currentAmount, runtime) -> None:
        self.stateID: int  = stateId
        self.ID: int  = id
        self.targetAmount: int = targetAmount
        self.currentAmount: int = currentAmount
        self.runtime:int = runtime

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
        return f"MyClass(stateID: {self.stateID}, id: {self.ID}, targetAmount: {self.targetAmount}, currentAmount: {self.currentAmount}, runtime: {self.runtime})"
    
    def getJson(self):
        return {
            "stateId": self.stateID,
            "id": self.ID,
            "targetAmount": self.targetAmount,
            "currentAmount": self.currentAmount,
            "runtime": self.runtime
        }