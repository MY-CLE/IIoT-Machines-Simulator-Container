from datetime import datetime
import json

from database.handler.databaseHandler import DatabaseHandler

class Warnings:
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
            self.possibleErrors.append(errorMessage)
        print("InitErrors complete")
        
    #in correct id order
    def initPossibleWarnings(self):
        for warningMessage in DatabaseHandler.selectWarningMessages():
            self.possibleWarnings.append(warningMessage)
        print("InitWarnings complete")      
    
    def coolantLvlWarning(self):
        warningMessage = self.possibleWarnings[0]
        warningTime = datetime.now()
        self.warnings.append((warningTime, warningMessage))
        print(warningMessage)

    def laserModuleWarning(self):
        warningMessage = self.possibleWarnings[1]
        warningTime = datetime.now()
        self.warnings.append((warningTime, warningMessage))
        print(warningMessage)

    def powerConsumptionWarning(self):
        warningMessage = self.possibleWarnings[2]
        warningTime = datetime.now()
        self.warnings.append((warningTime, warningMessage))
        print(warningMessage)

    def coolantLvlError(self):
        errorMessage = self.possibleErrors[0]
        errorTime = datetime.now()
        self.errors.append((errorTime, errorMessage))
        print(errorMessage)

    def laserModuleError(self):
        errorMessage = self.possibleErrors[1]
        errorTime = datetime.now()
        self.errors.append((errorTime, errorMessage))
        print(errorMessage)

    def powerConsumption(self):
        errorMessage = self.possibleErrors[2]
        errorTime = datetime.now()
        self.errors.append((errorTime, errorMessage))
        print(errorMessage)
        
    def setSelectedError(self, error_id):
        errorMessage = self.possibleErrors[int(error_id)]
        errorTime = datetime.now()
        self.errors.append((errorTime, errorMessage))
        print(errorMessage)
        print("Lenght of current Error List =" , len(self.errors))

    def setSelectedWarning(self, warning_id):
        warningMessage = self.possibleWarnings[int(warning_id)]
        warningTime = datetime.now()
        self.warnings.append((warningTime, warningMessage))
        print(warningMessage)
        print("Lenght of current Error List =" , len(self.warnings))
        
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