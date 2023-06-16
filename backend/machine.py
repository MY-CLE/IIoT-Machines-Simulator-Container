from datetime import datetime

class Machine():
    
    def __init__(self):
        
        #When stored/loaded in database
        self.machineStateId: int = None
        self.lastEdited = None
        self.machineStateName = None
        
        self.machineProtocol = None
        
        
        



    def getMachinStateId(self) -> int:
        return self.machineStateId

    def g