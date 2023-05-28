class Mode(object):

    def __init__(self, powerConsumptionKWH: int, laserModuleWeardown: int) -> None:
        self.powerConsumptionKWH: int = powerConsumptionKWH
        self.laserModuleWeardown: int = laserModuleWeardown

    def getPowerConsumptionKWH(self) -> int:
        return self.powerConsumptionKWH
    
    def getLaserModuleWeardown(self) -> int:
        return self.laserModuleWeardown
    