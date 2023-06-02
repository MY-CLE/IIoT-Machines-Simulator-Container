from mode import Mode
from triangle import Triangle
import time
from datetime import datetime
from times import Times
class Metrics(object):

    def __init__(self, coolantLevelPercent: int, simulationMode: Mode) -> None:
        self.coolantLevelPercent: int = coolantLevelPercent
        self.powerConsumptionKWH: int = simulationMode.getPowerConsumptionKWH()
        self.laserModuleWeardownPercent: int = simulationMode.getLaserModuleWeardown()
        self.timePerItem: int = simulationMode.getTimePerItem()
        self.totalItemsProduced: int = 0
        self.targetAmount: int = simulationMode.getTargetAmount()

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
    
    def getUptime(self) -> int:
        return 2
    
    def getCoolantConsumption(self) -> int:
        return 2
    
    def getTargetAmount(self) -> int:
        return self.targetAmount
    
    def updateMetrics(self, runtimeInSeconds: int) -> None:
        self.updateCoolantLevel()
        self.updatePowerConsumption(runtimeInSeconds)
        self.updateLaserModule(runtimeInSeconds)
        self.updateTotalItemsProduced(runtimeInSeconds, self.timePerItem)
        print(self.coolantLevelPercent)
        print(self.powerConsumptionKWH)
        print(self.laserModuleWeardownPercent)
        print(self.timePerItem)

    def updateCoolantLevel(self) -> None:
        self.coolantLevelPercent -= (self.laserModuleWeardownPercent / 120)

    def updatePowerConsumption(self, runtimeInSeconds: int) -> None:
        self.powerConsumptionKWH += (runtimeInSeconds / 60)

    def updateLaserModule(self, runtimeInSeconds: int) -> None:
        self.laserModuleWeardownPercent -= (runtimeInSeconds / 60)

    def updateTotalItemsProduced(self, runTimeInSeconds: int, timePerItem: int) -> None:
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
