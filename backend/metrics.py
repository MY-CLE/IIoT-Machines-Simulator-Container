from mode import Mode
from triangle import Triangle
import time
from datetime import datetime
from times import Times
class Metrics(object):

    def __init__(self, coolantLevelPercent: int, simulationMode: Mode) -> None:
        self.coolantLevelPercent: int = coolantLevelPercent
        #Luis
        self.powerConsumptionKWH: int = simulationMode.getPowerConsumptionKWH()
        self.laserModuleWeardownPercent: int = simulationMode.getLaserModuleWeardown()
        self.timePerItem: int = simulationMode.getTimePerItem()
        self.targetAmount: int = simulationMode.getTargetAmount()
        self.totalItemsProduced: int = 0
        #coolantConsumption gets calculated and depends on the laserModuleWeardownPercent which is, depending on what we 'produce' a standard amount coming from the DB
        #we devide that by 1200 (random)
        self.coolantCoolantConsumption = self.laserModuleWeardownPercent / 1200

    def setCoolantLevelPercent(self, coolantLevelPercent: int) -> None:
        self.coolantLevelPercent = coolantLevelPercent

    def setPowerConsumptionKWH(self, simulationMode: Mode) -> None:
        self.powerConsumptionKWH = simulationMode.getPowerConsumptionKWH()

    def setLaserModulePowerWeardown(self, simulationMode: Mode) -> None:
        self.laserModuleWeardownPercent = simulationMode.getLaserModuleWeardown()
    
    def setTotalItemsProduced(self, itemsProduced: int) -> None:
        self.totalItemsProduced = itemsProduced
    
    def getTotalItemsProduced(self) -> int:
        return self.totalItemsProduced

    def getCoolantLevelPercent(self) -> int:
        return (int)(round(self.coolantLevelPercent))
    
    def getPowerConsumptionKWH(self) -> int:
        return (int)(round(self.powerConsumptionKWH))

    def getLaserModulePowerWeardown(self) -> int:
        return (int)(round(self.laserModuleWeardownPercent))
    
    def getTimePerItem(self) -> int:
        return self.timePerItem
    
    def getCoolantConsumption(self) -> int:
        return int(self.coolantCoolantConsumption)
    
    def getTargetAmount(self) -> int:
        return self.targetAmount

    def updateMetrics(self, runtimeInSeconds: int) -> None:
        self.updateCoolantLevel()
        self.updatePowerConsumption(runtimeInSeconds)
        self.updateLaserModule(runtimeInSeconds)
        self.updateTotalItemsProduced(runtimeInSeconds, self.timePerItem)
        print("Coolant level percent: ", self.coolantLevelPercent)
        print("Power consumption in KWH: ", self.powerConsumptionKWH)
        print("Laser module weardown: ", self.laserModuleWeardownPercent)
        print("Time per item:", self.timePerItem)
        print("Total items produced:", self.totalItemsProduced)

    def updateCoolantLevel(self) -> None:
        #substract coolantConsumption from coolantLevel
        self.coolantLevelPercent -= self.coolantCoolantConsumption

    def updatePowerConsumption(self, runtimeInSeconds: int) -> None:
        #add powerConsumption up depending on how long the machine is running
        self.powerConsumptionKWH += (runtimeInSeconds / 60)

    def updateLaserModule(self, runtimeInSeconds: int) -> None:
        #substract laserModuleWeardown depending on how long the machine is running
        self.laserModuleWeardownPercent -= (runtimeInSeconds / 60)

    def updateTotalItemsProduced(self, runTimeInSeconds: int, timePerItem: int) -> None:
        #we calculate totalItemsProduced by dividing the runTime with timePerItem which we both get as parameters
        self.totalItemsProduced = int(runTimeInSeconds / timePerItem)

if __name__ == "__main__":
    metrics = Metrics(100, Triangle())
    times = Times(datetime.now(), 0)
    while True:
        time.sleep(5)
        times.calculateRunTime(datetime.now())
        metrics.updateMetrics(times.getRuntime())
        print("PowerConsumptionKWH: ", metrics.getPowerConsumptionKWH())
        print("LaserModulePowerWeardown: ", metrics.getLaserModulePowerWeardown())
        print("CoolantLevelPercent: ", metrics.getCoolantLevelPercent())
        print("TotalItemsProduced: ", int(metrics.getTotalItemsProduced()))
