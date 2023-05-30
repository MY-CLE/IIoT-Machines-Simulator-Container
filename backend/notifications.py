from datetime import datetime

class Warnings(object):
    def __init__(self) -> None:    
        self.errors = []
        self.warnings = []

    def getErrors(self) -> list:
        return self.errors
    
    def getWarnings(self) -> list:
        return self.warnings
    
    def coolantLvlWarning(self):
        warningMessage = "Coolant Level below 10%. Please refill!"
        warningTime = datetime.now()
        self.warnings.append((warningTime, warningMessage))
        print(warningMessage)

    def laserModuleWarning(self):
        warningMessage = "Laser module power below 10%. Please swap module!"
        warningTime = datetime.now()
        self.warnings.append((warningTime, warningMessage))
        print(warningMessage)

    def powerConsumptionWarning(self):
        warningMessage = "Power Consumption is getting high. Please take a break!"
        warningTime = datetime.now()
        self.warnings.append((warningTime, warningMessage))
        print(warningMessage)

    def coolantLvlError(self):
        errorMessage = "Coolant empty. Machine is stopping!"
        errorTime = datetime.now()
        self.errors.append((errorTime, errorMessage))
        print(errorMessage)

    def laserModuleError(self):
        errorMessage = "Laser module burnt out. Machine is stopping!"
        errorTime = datetime.now()
        self.errors.append((errorTime, errorMessage))
        print(errorMessage)

    def powerConsumption(self):
        errorMessage = "Power consumption significantly too high. Machine is stopping!"
        errorTime = datetime.now()
        self.errors.append((errorTime, errorMessage))
        print(errorMessage)

if __name__ == "__main__":
    warning = Warnings()
    warning.coolantLvlError()