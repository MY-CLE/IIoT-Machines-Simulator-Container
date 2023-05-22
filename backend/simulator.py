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
        self.stromverbrauch = 0.0 #in kH/h?
        self.laserLeistung = 100 #100%
        self.luftdruck = 5 #bar
        self.temperatur = 80 #Grad Celcius
        
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

    def simulierSafetyDoorError(self):
        timeInterval = random.randint(0, 15)
        time.sleep(timeInterval)
        raise Exception("Safety door open!")
    
    def exceptionHandler(self, exc_type, exc_value, traceback):
        if exc_type is not KeyboardInterrupt:
            try:
                self.simulierSafetyDoorError()
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

    def berechneSimDauer(self, stückzahl: int, produktionsZeit: int) -> int:
        simDauer = 0
        for i in range(produktionsZeit):
            simDauer += produktionsZeit
        
        simDauer = round(simDauer * 1.1)
        return simDauer
    
    def kühlwasserWarnung(self):
        fehlermeldung = "Kühlwasser ist unter 20%. Bitte nachfüllen."
        fehlerZeit = datetime.now()
        self.log.append((fehlerZeit, fehlermeldung))
        print(f"Fehlerzeit: {fehlerZeit}, Fehlermeldung: {fehlermeldung}")

    def programSimulation(self, currentTime: datetime, sollStückzahl: int, produktionsstück: str):
        produktionsZeit = 5 #benutzt um produktionszeit von einem Stück zu berechnen, unterschiedliche Produktionszeit für unterschiedliche Endprodukte
        if produktionsstück == "dreieck":
            produktionsZeit = 3
        elif produktionsstück == "kreis":
            produktionsZeit = 5
        elif produktionsstück == "viereck":
            produktionsZeit = 6

        simDauer = self.berechneSimDauer(sollStückzahl, produktionsZeit) #simDauer für Berechnung von Verbrauchen
        dummy, stromverbrauchProStück = self.berechneStromverbauch(sollStückzahl, produktionsZeit)
        programmStromverbrauch = 0.0

        try:
            #Schleife um Produktion von gegebener Stückzahl zu simulieren
            for i in range(sollStückzahl):
                time.sleep(produktionsZeit)
                self.stückzahl += 1

                programmStromverbrauch += stromverbrauchProStück

                wasserVerbrauch = simDauer / 60 #Verbrauch pro Sekunde
                self.kühlwasserstand = self.kühlwasserstand - wasserVerbrauch #Verbrauch von aktuellem Stand abziehen
                print("Kühlwasserstand: ", self.kühlwasserstand)
                print("Stückzahl: ", self.stückzahl)

                #falls Kühlwasser leer wird, error message -> log und maschine stoppt aufgerufen
                if self.kühlwasserstand < 20:
                    self.kühlwasserWarnung()
                    self.stopMachine()
                    break
                
                #Prüfung ob Programm abgeschlossen ist
                if i == sollStückzahl - 1:
                    self.stromverbrauch, dummy = self.berechneStromverbauch(sollStückzahl, produktionsZeit) #Stromverbrauch erst berechnen wenn Programm abgeschlossen ist
                    print("Programm erfolgreich abgeschlossen")
                    print("\nStromverbrauch von Programm in kW: ", programmStromverbrauch)
                    self.stopMachine() 
        except Exception as e:
            print("Fehler bei der Programmsimulation: ", str(e))


    def berechneStromverbauch(self, sollStückzahl: int, produktionsZeit: int):
        #je nachdem wie lange produktion von einem Stück braucht, desto höher der Verbrauch
        if produktionsZeit == 3:
            stromverbrauchProStück = 0.5 #0.5 kW pro Minute
        elif produktionsZeit == 5:
            stromverbrauchProStück = 0.7
        elif produktionsZeit == 6:
            stromverbrauchProStück = 0.8

        stromverbrauchProStunde = stromverbrauchProStück * 3600 #umrechnung auf kW/h
        
        return stromverbrauchProStunde, stromverbrauchProStück


if __name__ == "__main__":
    machineSimu = Simulator()
    machineSimu.startMachine()
    time.sleep(3)
    now = time.time()
    machineSimu.programSimulation(now, 5, "dreieck")
    print("Laufzeit der Maschine: ", machineSimu.getLaufzeit())
    print("Stromverbrauch in kW/h: ", machineSimu.getStromverbrauch())    
    
    #machineSimu.simulierSafetyDoorError()
    #time.sleep(20)
    #machineSimu.stopMachine()
    #print("Machine runtime: " + str(machineSimu.getRuntime()) + " seconds.")
