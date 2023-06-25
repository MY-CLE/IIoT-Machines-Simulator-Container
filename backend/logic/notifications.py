from datetime import datetime
import json

from database.handler.databaseHandler import DatabaseHandler

class Notifications(object):
    def __init__(self) -> None:    
        self.errors = []
        self.warnings = []
        self.possibleErrors = []
        self.possibleWarnings = []
        self.initPossibleErrors()
        self.initPossibleWarnings()

    def getErrors(self) -> list:
        return self.errors
    
    def getWarnings(self) -> list:
        return self.warnings
    
    def getPossibleErrors(self) -> list:
        return self.possibleErrors
    
    def getPossibleWarnings(self) -> list:
        return self.possibleWarnings
    
    #in correct id order
    def initPossibleErrors(self):
        for errorMessage in DatabaseHandler.selectErrorMessages():
            self.possibleErrors.append(errorMessage.getType())
        
    #in correct id order
    def initPossibleWarnings(self):
        for warningMessage in DatabaseHandler.selectWarningMessages():
            self.possibleWarnings.append(warningMessage.getType())  
    
    def coolantLvlWarning(self):
        warningMessage = self.possibleWarnings[0]
        if not self.checkExistingWarnings(warningMessage):
            warningTime = datetime.now()
            self.warnings.append((warningTime, warningMessage))

    def laserModuleWarning(self):
        warningMessage = self.possibleWarnings[1]
        if not self.checkExistingWarnings(warningMessage):
            warningTime = datetime.now()
            self.warnings.append((warningTime, warningMessage))

    def powerConsumptionWarning(self):
        warningMessage = self.possibleWarnings[2]
        if not self.checkExistingWarnings(warningMessage):
            warningTime = datetime.now()
            self.warnings.append((warningTime, warningMessage))

    def coolantLvlError(self):
        errorMessage = self.possibleErrors[0]
        if not self.checkExistingErrors(errorMessage):
            errorTime = datetime.now()
            self.errors.append((errorTime, errorMessage))

    def laserModuleError(self):
        errorMessage = self.possibleErrors[1]
        if not self.checkExistingErrors(errorMessage):
            errorTime = datetime.now()
            self.errors.append((errorTime, errorMessage))

    def SafetyDoorError(self):
        errorMessage = self.possibleErrors[2]
        if not self.checkExistingErrors(errorMessage):
            errorTime = datetime.now()
            self.errors.append((errorTime, errorMessage))
        
    def setSelectedError(self, error_id):
        errorMessage = self.possibleErrors[int(error_id)]
        if not self.checkExistingErrors(errorMessage):          
            errorTime = datetime.now()
            self.errors.append((errorTime, errorMessage))


    def setSelectedWarning(self, warning_id):
        warningMessage = self.possibleWarnings[int(warning_id)]
        if not self.checkExistingWarnings(warningMessage):
            warningTime = datetime.now()
            self.warnings.append((warningTime, warningMessage))
        
        
    def checkExistingErrors(self, errorMessage):
        for index, message in enumerate(self.errors):
            if message[1] is errorMessage:
                return True
        return False
        
        
    def checkExistingWarnings(self, warningMessage):
        for index, message in enumerate(self.warnings):
            if message[1] is warningMessage:
                return True
        return False
    
    def getNotificationsJSON(self):
        data = {
            "errors": [],
            "warnings": []
        }
        for index in range(0,len(self.possibleErrors)):
            error = self.possibleErrors[index]
            error_data = {
                "id": str(index),
                "name": error
            }
            data["errors"].append(error_data)
            
        for index in range(0,len(self.possibleWarnings)):
            warning = self.possibleWarnings[index]
            warning_data = {
                "id": str(index),
                "name": warning
            }
            data["warnings"].append(warning_data)
        
        print(data)   
        return json.dumps(data)
            
            
            
            

if __name__ == "__main__":
    warning = Warnings()
    warning.getNotificationsJSON()
    warning.setSelectedError("1")
    print(warning.getErrors())
    
    
#Error & Warning Mapping:
    #Warings:
            #id = 0 -> "Coolant Level below 10%. Please refill!"
            #id = 1 -> "Laser module power below 10%. Please swap module!"
            #id = 2 -> "Power Consumption is getting high. Please take a break!"
    #Errors:
            #id = 0 -> "Coolant empty. Machine is stopping!"
            #id = 1 -> "Laser module burnt out. Machine is stopping!"
            #id = 2 -> "Power consumption significantly too high. Machine is stopping!"