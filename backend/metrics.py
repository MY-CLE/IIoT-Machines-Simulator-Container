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
        self.coolantCoolantConsumption = self.laserModuleWeardownPercent / 2500

    def setCoolantLevelPercent(self, coolantLevelPercent: int) -> None:
        self.coolantLevelPercent = coolantLevelPercent

    def setPowerConsumptionKWHMode(self, simulationMode: Mode) -> None:
        self.powerConsumptionKWH = simulationMode.getPowerConsumptionKWH()

    def setLaserModulePowerWeardownMode(self, simulationMode: Mode) -> None:
        self.laserModuleWeardownPercent = simulationMode.getLaserModuleWeardown()
    
    def setPowerConsumptionKWH(self, consumption: int) -> None:
        self.powerConsumptionKWH = consumption

    def setLaserModulePowerWeardown(self, consumption: int) -> None:
        self.laserModuleWeardownPercent = consumption

    def setTotalItemsProduced(self, itemsProduced: int) -> None:
        self.totalItemsProduced = itemsProduced

    def setTimePerItem(self, timePerItem: int) -> None:
        self.timePerItem = timePerItem
    
    def getTotalItemsProduced(self) -> int:
        return self.totalItemsProduced

    def getCoolantLevelPercent(self) -> int:
        return (int) (self.coolantLevelPercent)

    def getPowerConsumptionKWH(self) -> int:
        return (int)(self.powerConsumptionKWH)

    def getLaserModulePowerWeardown(self) -> int:
        return (int)(self.laserModuleWeardownPercent)
    
    def getTimePerItem(self) -> int:
        return self.timePerItem
    
    def getCoolantConsumption(self) -> int:
        return int(self.coolantCoolantConsumption)
    
    def getTargetAmount(self) -> int:
        return self.targetAmount

    def updateMetrics(self, runtimeInSeconds: int) -> None:
        self.updateCoolantLevel(runtimeInSeconds)
        self.updatePowerConsumption(runtimeInSeconds)
        self.updateLaserModule(runtimeInSeconds)
        self.updateTotalItemsProduced(runtimeInSeconds, self.timePerItem)
        print("Coolant level percent: ", self.coolantLevelPercent)
        print("Power consumption in KWH: ", self.powerConsumptionKWH)
        print("Laser module weardown: ", self.laserModuleWeardownPercent)
        print("Time per item:", self.timePerItem)
        print("Total items produced:", self.totalItemsProduced)

    def updateCoolantLevel(self, runtimeInSeconds: int) -> None:
    # Subtract coolantConsumption from coolantLevel
        self.coolantLevelPercent -= self.coolantCoolantConsumption * (runtimeInSeconds / 60)
    # Update powerConsumption based on coolantLevel
        self.powerConsumptionKWH += self.coolantLevelPercent * 0.01  

    def updatePowerConsumption(self, runtimeInSeconds: int) -> None:
    # Calculate powerConsumption based on runtimeInSeconds and laserModuleWeardown
        self.powerConsumptionKWH += runtimeInSeconds * (1 + self.laserModuleWeardownPercent / 100) * 0.02  

    def updateLaserModule(self, runtimeInSeconds: int) -> None:
    # Calculate laserModuleWeardown based on runtimeInSeconds and coolantLevel
        self.laserModuleWeardownPercent -= runtimeInSeconds * (self.coolantLevelPercent / 100) * 0.05  
    def updateTotalItemsProduced(self, runtimeInSeconds: int, timePerItem: int) -> None:
    # Calculate totalItemsProduced based on runtimeInSeconds, timePerItem, and powerConsumption
        self.totalItemsProduced = int(runtimeInSeconds / timePerItem) * (1 + self.powerConsumptionKWH / 100) 


""" if __name__ == "__main__":
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
 """