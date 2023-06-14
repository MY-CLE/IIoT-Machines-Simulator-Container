from datetime import datetime

class Times(object): 
    def __init__(self, startTime: datetime, idleTime: int) -> None:
        self.startTime = startTime
        self.stopTime = None
        self.runtime: int = 0
        self.idleTime: int = idleTime
        self.state: bool = False

    def getStartTime(self) -> datetime:
        return self.startTime
        
    def getStopTime(self) -> int:
        return self.stopTime
        
    def getRuntime(self) -> int:
        return int(self.runtime)
        
    def getIdleTime(self) -> int:
        return int(self.idleTime)
    
    def setState(self, bool: bool) -> None:
        self.state = bool
    
    def setRunTime(self, runtime: int) -> None:
        self.runtime = runtime
        
    def setStartTime(self, startTime: datetime) -> None:
        self.startTime = startTime
        self.state = True
    
    def setIdleTime(self, idleTime: int) -> None:
        self.idleTime = idleTime

    def setStopTime(self) -> None:
        self.stopTime = datetime.now()
        self.state = False
    
    def calculateRunTime(self, time: datetime) -> None:
        #first subtraction of time(current time) and startTime which gets set when initializing the object
        #then add result to runtime so it goes up
        self.runtime = self.runtime + (time - self.startTime).total_seconds()
        #set startTime to current time for next call of function
        self.startTime = time

    def calculateIdleTime(self, time: datetime) -> int:
        #check if stopTime is none to set idleTime to 0, if stopTime exists calculate idleTime with current time
        if self.stopTime == None:
            self.idleTime = 0
        else:
            if self.state == True:
                return self.idleTime
            #first substract time from stopTime which gets set when stopMachine function gets called
            #then add result of that calculation to idleTime so it increases
            self.idleTime = self.idleTime + (time - self.stopTime).total_seconds()
            #stopTime gets set to current time to prepare for next call
            self.stopTime = time
        return self.idleTime
