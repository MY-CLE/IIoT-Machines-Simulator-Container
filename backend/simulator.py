from datetime import datetime 
import random
import time
import sys

parameterMap ={
    0: "runTime",
    1: "coolantLevel",
    2: "powerConsumption",
    3: "laserModulePower",
    4: "standstillTime",
    5: "errorState",
    6: "privilegeState"
}

class Simulator: 
    def __init__(self):
        self.startTime = datetime.now()
        self.stopTime = None
        self.runTime: int = 0
        self.standstillTime: int = 0

        self.coolantLevel = 100 #100%
        self.quantity = 0
        self.powerConsumption = 0.0 #in kH/h?
        self.laserModulePower = 100 #100%
        
        self.errorState = False
        self.privilegeState = False
        self.errors = []
        self.securityWarnings = []
        self.state = False
        self.log = []

    def getStartzeit(self):
        return self.startTime
    
    def getStopTime(self):
        return self.stopTime
    
    def getStandstillTime(self):
        return self.standstillTime
    
    def getRunTime(self):
        return self.runTime
    
    def getTotalRunTime(self):
        return self.totalRunTime

    def getCoolantLevel(self):
        return self.coolantLevel
    
    def getQuantity(self):
        return self.quantity

    def getPowerConsumption(self):
        return self.powerConsumption

    def getLaserModulePower(self):
        return self.laserModulePower

    def getFehler(self):
        return self.errors
    
    def getSicherheitswarungen(self):
        return self.securityWarnings
    
    def getStatus(self):
        return self.state
    
    def getLog(self):
        return self.log
    
    def getErrorState(self):
        return self.errorState
    
    def getPrivilegeState(self):
        return self.privilegeState
    
    def setRunTime(self, runTime: int):
        self.runTime = runTime

    def updateSimulation(self, time):
        
        self.runTime: int = self.runTime + (time - self.startTime).total_seconds()
        self.startTime = time
        self.state = True
        self.reduceCoolantConsumption(self.runTime)
        self.laserModuleWearDown(self.runTime)
        self.calculatePowerConsumption(self.runTime)

    #return of JSON
    def getMachineState(self):
        return self.__json__()
    
    def setParameter(self, id, value):
        setattr(self, parameterMap[id], value)
    def simulateSafetyDoorError(self):
        timeInterval = random.randint(0, 15)
        time.sleep(timeInterval)
        raise Exception("Safety door open!")
    
    def exceptionHandler(self, exc_type, exc_value, traceback):
        if exc_type is not KeyboardInterrupt:
            try:
                self.simulateSafetyDoorError()
            except Exception as e:
                print("Error occurred while simulating. Error:", e)
                if self.state:
                    self.stopMachine()
                    print("Machine runTime: " + str(self.getRuntime()) + " seconds.")

    def startMachine(self):
        #sys.excepthook = self.exceptionHandler
        print("Starting the Machine...")
        self.state = True
        self.startTime = datetime.now()
        #
        #
        print("Machine is running.")
    
    def stopMachine(self):
        print("Stopping the Machine...")
        self.stopTime = datetime.now()
        #
        #
        #
        self.calculateRunTime()
        self.state = False
        print("Machine stopped.")

    def calculateRunTime(self):
        self.runTime = self.stopTime - self.startTime

    def calculateSimLength(self, quantity: int, productionTime: int) -> int:
        simLength = 0
        resetTimeLaser = 0.1 #Annahme Lasermodul braucht kurz um wieder zu resetten
        for i in range(quantity):
            simLength += productionTime + resetTimeLaser
        
        simLength = round(simLength * 1.1) #*1.1 um Puffer einzubauen/einzurechnen
        return simLength
    
    def coolantWarning(self):
        errorMessage = "Kühlwasser ist unter 20%. Bitte nachfüllen."
        errorTime = datetime.now()
        self.log.append((errorTime, errorMessage))
        print(f"errorTime: {errorTime}, errorMessage: {errorMessage}")

    def laserModuleWarning(self):
        errorMessage = "Laser Modul abgenutzt. Bitte wechseln."
        errorTime = datetime.now()
        self.log.append((errorTime, errorMessage))
        print(f"errorTime: {errorTime}, errorMessage: {errorMessage}")

    def laserModuleWearDown(self, simLength: float):
        laserWeardown = simLength / 40 #simulier die Abnutzung vom Laser Module je nachdem wie lange das Programm ist und der Teiler gewählt wird
        self.laserModulePower -= laserWeardown #Verbrauch von aktuellem Stand abziehen
        if self.laserModulePower < 20:
            self.laserModuleWarning()

    def reduceCoolantConsumption(self, simLength: float):
        coolantConsumption = simLength / 30  #coolantConsumption, teiler flexibel(evtl variabel?)
        self.coolantLevel -= coolantConsumption #Verbrauch von aktuellem Stand abziehen
        if self.coolantLevel < 20:
            self.coolantWarning()

    def programSimulation(self, currentTime: datetime, targetAmount: int, endProduct: str):
        productionTime = 5 #benutzt um productionTime von einem Stück zu berechnen, unterschiedliche productionTime für unterschiedliche Endprodukte
        if endProduct == "dreieck":
            productionTime = 3
        elif endProduct == "kreis":
            productionTime = 5
        elif endProduct == "viereck":
            productionTime = 6

        simLength = self.calculateSimLength(targetAmount, productionTime) #simLength von Pogramm für Berechnung von Verbrauchen
        powerConsumptionApiece = self.calculatePowerConsumption(productionTime)
        powerConsumptionProgram = 0

        try:
            #Schleife um Produktion von gegebener quantity zu simulieren
            for i in range(targetAmount):
                time.sleep(productionTime) #Zeit für die Produktion
                self.quantity += 1 

                powerConsumptionProgram += powerConsumptionApiece #Berechnung Stromverbrauch von Programm

                self.laserModuleWearDown(simLength, 30) #simulier die Abnutzung vom Laser Module je nachdem wie lange das Programm ist und der Teiler gewählt wird
                self.reduceCoolantConsumption(simLength, 60) #coolantConsumption, teiler flexibel(evtl variabel?)
                
                print("LaserModulePower: ", round(self.laserModulePower, 2))
                print("CoolantLevel: ", round(self.coolantLevel, 2))
                print("Quantity: ", self.quantity)

                #falls Kühlwasser leer wird, errors message -> log und maschine stoppt aufgerufen
                if self.coolantLevel < 20:
                    self.coolantWarning()
                    self.stopMachine()
                    break
                
                #falls Laser Modul zu abgenutzt ist, errors message -> log und maschine stoppt aufgerufen
                if self.laserModulePower < 20:
                    self.laserModuleWarning()
                    self.stopMachine()
                    break

                #Prüfung ob Programm abgeschlossen ist
                if i == targetAmount - 1:
                    #self.powerConsumption = self.calculatePowerConsumption(productionTime) #Stromverbrauch Berechnung 
                    self.powerConsumption = powerConsumptionProgram
                    print("Programm erfolgreich abgeschlossen")
                    self.stopMachine() 
        except Exception as e:
            print("Fehler bei der Programmsimulation: ", str(e))

    def calculatePowerConsumption(self, simLength: float):
        powerConsumption = simLength / 10
        self.powerConsumption += powerConsumption
        if self.powerConsumption > 70000:
            print("Warning! High Level of use. Strongly advice to take a break")
    
    def __json__(self):
        return {
            "parameters": [   
                {
                    "id": "0",
                    "description": "runTime",
                    "value": round(self.runTime, 2)
                },
                {
                    "id": "1",
                    "description": "coolant_level",
                    "value": round(self.coolantLevel, 2)
                },
                {
                    "id": "2",
                    "description": "power_consumption",
                    "value": round(self.powerConsumption, 2)
                },
                {
                    "id": "3",
                    "description": "power_laser_module",
                    "value": round(self.laserModulePower, 2),
                },
                {
                    "id": "4",
                    "description": "Standstill_time",
                    "value": self.standstillTime
                },
                {
                    "id": "5",
                    "description": "error_state",
                    "value": self.errorState
                },
                {
                    "id": "6",
                    "description": "privilage_state",
                    "value": self.privilegeState
                }
            ],
            "error_state": {
                "errors": [
                    {
                        "error_id": 0
                    }
                ],
                "warnings": [
                    {
                        "error_id": 0
                    }
                ]
            }
        }

    


if __name__ == "__main__":
    machineSimu = Simulator()
    machineSimu.startMachine()
    time.sleep(3)
    now = time.time()
    machineSimu.programSimulation(now, 6, "dreieck")
    print("Laufzeit des Programmes: ", machineSimu.getRunTime())
    print("Power Consumption of Program in kW: ", machineSimu.getPowerConsumption())


    #machineSimu.simulateSafetyDoorError()
    #time.sleep(20)
    #machineSimu.stopMachine()
    #print("Machine runTime: " + str(machineSimu.getRuntime()) + " seconds.")
