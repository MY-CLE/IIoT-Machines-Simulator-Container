import time
import random
import sys

class Simulator: 
    def __init__(self) -> None:
        self.startTime = None
        self.stopTime = None
        self.runTime = 0
        self.isRunning = False

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
                if self.isRunning:
                    self.stopMachine()
                    print("Machine runtime: " + str(self.getRuntime()) + " seconds.")

    def startMachine(self):
        sys.excepthook = self.exceptionHandler
        print("Starting the Machine...")
        self.isRunning = True
        self.startTime = time.time()
        #
        #
        print("Machine is running.")
    
    def stopMachine(self):
        print("Stopping the Machine...")
        self.stopTime = time.time()
        #
        #
        #
        self.calculateRuntime()
        self.isRunning = False
        print("Machine stopped.")

    def calculateRuntime(self):
        self.runTime = round(self.stopTime - self.startTime, 2)

    def getRuntime(self):
        self.calculateRuntime()
        return self.runTime



machineSimu = Simulator()
machineSimu.startMachine()
machineSimu.simulateSafetyDoorError()
time.sleep(20)
machineSimu.stopMachine()
print("Machine runtime: " + str(machineSimu.getRuntime()) + " seconds.")
