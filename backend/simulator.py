from datetime import datetime 
import random
import time
import sys
#sys.path.append("backend\\opcuaIRF\\")
import threading
import logging
from metrics import Metrics
from times import Times
from triangle import Triangle
from mode import Mode
from notifications import Warnings
from opcuaIRF.opcuaServer import OPCUAServer
from opcuaIRF.opcuaClient import OPCUAClient

from modbusIRF.modbusServer import ModbusTCPServer
from modbusIRF.modbusClient import ModbusTCPClient

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')

parameterMap ={
    0: "runTime",
    1: "coolantLevel",
    2: "powerConsumption",
    3: "laserModulePower",
    4: "standstillTime",
    5: "errorState",
    6: "privilegeState"
}

class Simulator: 
    def __init__(self, simulationMode: Mode):
        self.state = True
        
        self.metrics: Metrics = Metrics(100, simulationMode)
        self.warnings: Warnings = Warnings()

        self.times: Times = Times(datetime.now(), 0)

        self.opcuaServerThread = threading.Thread(target=self.startOPCUAServer)

        self.modbusServerThread = threading.Thread(target=self.startModbusServer)
        
        self.opcuaServerThread.start()
        self.modbusServerThread.start()

    def stopSimulator(self) -> None:
        self.times.setStopTime()
        print("Machine stopped!")
        self.state = False

    def startSimulator(self) -> None:
        self.state = True

    def startOPCUAServer(self):
        self.ouaServer = OPCUAServer()
        self.ouaServer.setParameter()
        self.ouaServer.server.start()
        logging.info("Server started")

    def startModbusServer(self):
        self.modbusServer = ModbusTCPServer()
        self.modbusServer.startServer()
        self.modbusServer.logServerChanges(0, 10)
        logging.info("Server started")

    def updateSimulation(self, time: datetime) -> None:
        self.times.calculateRunTime(time)
        runTime = self.times.getRunTime()
        self.metrics.updateMetrics(runTime)
        
        self.checkErrors()
        self.checkWarnings()
        
        self.ouaClient = OPCUAClient()
        logging.info("Client started")
        self.ouaClient.changeParam("Runtime", int(runTime))
        self.ouaClient.getParam()
        self.ouaClient.client.disconnect()

        self.modbusClient = ModbusTCPClient()
        logging.info("ModbusTCPClient started")
        self.modbusClient.writeSingleRegister(0, int(runTime))
        self.modbusClient.readHoldingRegisters(0, 10)

    def checkErrors(self) -> None:
        if self.metrics.getCoolantLevelPercent() <= 0:
            self.warnings.coolantLvlError()
            self.stopSimulator()
        if self.metrics.getPowerConsumptionKWH() >= 1000:
            self.warnings.powerConsumption()
            self.stopSimulator()
        if self.metrics.getLaserModulePowerWeardown() <= 0:
            self.warnings.laserModuleError()
            self.stopSimulator()

    def checkWarnings(self) -> None: 
        if self.metrics.getCoolantLevelPercent() <= 10:
            self.warnings.coolantLvlWarning()
        if self.metrics.getPowerConsumptionKWH() >= 900:
            self.warnings.powerConsumptionWarning()
        if self.metrics.getLaserModulePowerWeardown() <= 10:
            self.warnings.laserModuleWarning()


    #return of JSON
    def getMachineState(self):
        return self.__json__()
    
    def __json__(self):
        return {
            "parameters": [   
                {
                    "id": "0",
                    "description": "run_time",
                    "value": round(self.times.getRunTime())
                },
                {
                    "id": "1",
                    "description": "coolant_level",
                    "value": self.metrics.getCoolantLevelPercent()
                },
                {
                    "id": "2",
                    "description": "power_consumption",
                    "value": self.metrics.getPowerConsumptionKWH()
                },
                {
                    "id": "3",
                    "description": "power_laser_module",
                    "value": self.metrics.getLaserModulePowerWeardown()
                },
                {
                    "id": "4",
                    "description": "Standstill_time",
                    "value": self.times.calculateIdleTime(datetime.now())
                },
                {
                    "id": "5",
                    "description": "error_state",
                    "value": self.warnings.getErrors()
                },
                {
                    "id": "6",
                    "description": "privilege_state",
                    "value": 0
                }
            ],
            "error_state": {
                "errors": [
                    {
                        "error_id": 0
                    }
                ],
                "warnings": [
                    {
                        "error_id": 0
                    }
                ]
            }
        }

    


if __name__ == "__main__":
    machine = Simulator(Triangle())
    while True:
        time.sleep(3)
        machine.updateSimulation(datetime.now())
    
