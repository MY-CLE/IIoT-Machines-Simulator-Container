class Mode(object):

    def __init__(self, powerConsumptionKWH: int, laserModuleWeardown: int, timePerItem: int) -> None:
        self.timePerItem: int = timePerItem
        self.powerConsumptionKWH: int = powerConsumptionKWH
        self.laserModuleWeardown: int = laserModuleWeardown

    def getTimePerItem(self) -> int:
        return self.timePerItem

    def getPowerConsumptionKWH(self) -> int:
        return self.powerConsumptionKWH
    
    def getLaserModuleWeardown(self) -> int:
        return self.laserModuleWeardown
    