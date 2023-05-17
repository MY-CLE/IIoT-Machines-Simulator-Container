import time
import random
import sys

class Simulator: 
    def __init__(self) -> None:
        self.startzeit = 0
        self.stopzeit = 0
        self.laufzeit = 0
        self.stillstandzeit = 0

        self.kühlwasserstand
        self.stückzahl
        self.stromverbrauch
        self.laserLeistung
        self.luftdruck
        self.temperatur
        
        self.fehler = []
        self.sicherheitswarnungen
        self.status
        self.log = []

    def getStartzeit(self):
        return self.startzeit
    
    def getStopzeit(self):
        return self.stopzeit
    
    def getLaufzeit(self):
        return self.laufzeit
    
    def getStillstandszeit(self):
        return self.stillstandzeit
    
    def getKühlwasserstand(self):
        return self.kühlwasserstand
    
    def getStückzahl(self):
        return self.stückzahl

    def getStromverbrauch(self):
        return self.stromverbrauch

    def getLaserLeistung(self):
        return self.laserLeistung

    def getLuftdruck(self):
        return self.luftdruck

    def getTemperatur(self):
        return self.temperatur

    def getFehler(self):
        return self.fehler
    
    def getSicherheitswarungen(self):
        return self.sicherheitswarnungen
    
    def getStatus(self):
        return self.status
    
    def getLog(self):
        return self.log

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
                if self.status:
                    self.stopMachine()
                    print("Machine runtime: " + str(self.getRuntime()) + " seconds.")

    def startMachine(self):
        sys.excepthook = self.exceptionHandler
        print("Starting the Machine...")
        self.status = True
        self.startzeit = time.time()
        #
        #
        print("Machine is running.")
    
    def stopMachine(self):
        print("Stopping the Machine...")
        self.stopzeit = time.time()
        #
        #
        #
        self.calculateRuntime()
        self.status = False
        print("Machine stopped.")

    def calculateRuntime(self):
        self.laufzeit = round(self.stopzeit - self.startzeit, 2)

    def getRuntime(self):
        self.calculateRuntime()
        return self.laufzeit


if __name__ == "__main__":
    machineSimu = Simulator()
    machineSimu.startMachine()
    machineSimu.simulateSafetyDoorError()
    time.sleep(20)
    machineSimu.stopMachine()
    print("Machine runtime: " + str(machineSimu.getRuntime()) + " seconds.")
