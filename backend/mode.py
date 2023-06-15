
#define blueprint class for a simulation mode the simulator can work with
#capsules all necessary metrics to produce simulationMode specific data
class Mode(object):

    def __init__(self, powerConsumptionKWH: int, laserModuleWeardown: int, timePerItem: int, targetAmount: int) -> None:
        self.timePerItem: int = timePerItem
        self.powerConsumptionKWH: int = powerConsumptionKWH
        self.laserModuleWeardown: int = laserModuleWeardown
        self.targetAmount: int = targetAmount

    def getTimePerItem(self) -> int:
        return self.timePerItem

    def getPowerConsumptionKWH(self) -> int:
        return self.powerConsumptionKWH
    
    def getLaserModuleWeardown(self) -> int:
        return self.laserModuleWeardown
    
    def getTargetAmount(self) -> int:
        return self.targetAmount
    