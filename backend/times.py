from datetime import datetime

class Times(object): 
    def __init__(self, startTime: datetime, idleTime: int) -> None:
        self.startTime = startTime
        self.stopTime = None
        self.runtime: int = 0
        self.idleTime: int = idleTime

    def getStartTime(self) -> datetime:
        return self.startTime
        
    def getStopTime(self) -> int:
        return self.stopTime
        
    def getRuntime(self) -> int:
        return self.runtime
        
    def getIdleTime(self) -> int:
        return self.idleTime
    
        
    def setStopTime(self) -> None:
        self.stopTime = datetime.now()
    
    def calculateRunTime(self, time: datetime) -> None:
        self.runtime = self.runtime + (time - self.startTime).total_seconds()
        self.startTime = time

    def calculateIdleTime(self, time: datetime) -> int:
        if(self.stopTime == None):
            self.idleTime = 0
        else:
            self.idleTime = self.idleTime + (time - self.stopTime).total_seconds()
            self.stopTime = time
        return self.idleTime
