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

    def getCoolantLevelPercent(self) -> int:
        return (int)(round(self.coolantLevelPercent))
    
    def getPowerConsumptionKWH(self) -> int:
        return (int)(round(self.powerConsumptionKWH))

    def getLaserModulePowerWeardown(self) -> int:
        return (int)(round(self.laserModuleWeardownPercent))
    
    def updateMetrics(self, runtimeInSeconds: int) -> None:
        self.updateCoolantLevel()
        self.updatePowerConsumption(runtimeInSeconds)
        self.updateLaserModule(runtimeInSeconds)
        print(self.coolantLevelPercent)
        print(self.powerConsumptionKWH)
        print(self.laserModuleWeardownPercent)

    def updateCoolantLevel(self) -> None:
        self.coolantLevelPercent -= (self.laserModuleWeardownPercent / 120)

    def updatePowerConsumption(self, runtimeInSeconds: int) -> None:
        self.powerConsumptionKWH += (runtimeInSeconds / 60)

    def updateLaserModule(self, runtimeInSeconds: int) -> None:
        self.laserModuleWeardownPercent -= (runtimeInSeconds / 60)


if __name__ == "__main__":
    metrics = Metrics(100, Triangle())
    times = Times(datetime.now(), 0)
    while True:
        time.sleep(5)
        times.calculateRunTime(datetime.now())
        metrics.updateMetrics(times.getRuntime())
        print(metrics.getPowerConsumptionKWH())
        print(metrics.getLaserModulePowerWeardown())
        print(metrics.getCoolantLevelPercent())
