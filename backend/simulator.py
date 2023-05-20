from datetime import datetime 
import random
import time
import sys

class Simulator: 
    def __init__(self):
        self.startzeit = datetime
        self.stopzeit = datetime
        self.laufzeit = datetime
        self.stillstandzeit = 0

        self.kühlwasserstand = 100 #100%
        self.stückzahl = 0
        self.stromverbrauch = 0
        self.laserLeistung = 100
        self.luftdruck = 5
        self.temperatur = 80
        
        self.fehler = []
        self.sicherheitswarnungen = []
        self.status = True
        self.log = []

    def getStartzeit(self):
        return self.startzeit
    
    def getStopzeit(self):
        return self.stopzeit
    
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
        #sys.excepthook = self.exceptionHandler
        print("Starting the Machine...")
        self.status = True
        self.startzeit = datetime.now()
        #
        #
        print("Machine is running.")
    
    def stopMachine(self):
        print("Stopping the Machine...")
        self.stopzeit = datetime.now()
        #
        #
        #
        self.berechneLaufzeit()
        self.status = False
        print("Machine stopped.")

    def berechneLaufzeit(self):
        self.laufzeit = self.stopzeit - self.startzeit

    def getLaufzeit(self):
        return self.laufzeit

    def calculateSimDauer(self, stückzahl: int, sleepTime: int) -> int:
        simDauer = 0
        for i in range(sleepTime):
            simDauer += sleepTime
        
        simDauer = round(simDauer * 1.1)
        return simDauer
    
    def kühlwasserWarnung(self):
        fehlermeldung = "Kühlwasser ist unter 20%. Bitte nachfüllen."
        fehlerZeit = datetime.now()
        self.log.append((fehlerZeit, fehlermeldung))
        print(f"Fehlerzeit: {fehlerZeit}, Fehlermeldung: {fehlermeldung}")

    def programCircle(self, currentTime: datetime, sollStückzahl: int, produktionsstück: str):
        sleepTime = 5 #benutzt um produktionszeit von einem Stück zu berechnen
        if produktionsstück == "kreis":
            sleepTime = 5
        elif produktionsstück == "dreieck":
            sleepTime = 3
        elif produktionsstück == "viereck":
            sleepTime = 6

        simDauer = self.calculateSimDauer(sollStückzahl, sleepTime) #simDauer für Berechnung von Verbrauchen
        #Schleife um Produktion von gegebener Stückzahl zu simulieren
        for i in range(sollStückzahl):
            time.sleep(sleepTime)
            self.stückzahl += 1

            verbrauch = simDauer / 60 #Verbrauch pro Sekunde
            self.kühlwasserstand = self.kühlwasserstand - verbrauch #Verbrauch von aktuellem Stand abziehen
            print("Kühlwasserstand: ", self.kühlwasserstand)
            print("Stückzahl: ", self.stückzahl)

            #falls Kühlwasser leer wird, error message -> log und maschine stoppt aufgerufen
            if self.kühlwasserstand < 20:
                self.kühlwasserWarnung()
                self.stopMachine()
                break
            
            if i == sollStückzahl - 1:
                print("Programm erfolgreich abgeschlossen")
                self.stopMachine() 
        
       
if __name__ == "__main__":
    machineSimu = Simulator()
    machineSimu.startMachine()
    time.sleep(3)
    now = time.time()
    machineSimu.programCircle(now, 5, "dreieck")
    print("Laufzeit der Maschine: ", machineSimu.getLaufzeit())
    print(machineSimu.getLog())
    
    
    #machineSimu.simulateSafetyDoorError()
    #time.sleep(20)
    #machineSimu.stopMachine()
    #print("Machine runtime: " + str(machineSimu.getRuntime()) + " seconds.")
