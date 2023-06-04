from datetime import datetime
import json 
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
    5: "privilegeState",
    6: "timePerItem",
    7: "totalItems"
}

class Simulator: 
    def __init__(self, simulationMode: Mode):
        self.state = True
        self.simulationMode = simulationMode

        self.privilegeState: bool = False
        
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
    
    def getPrivilegeState(self) -> bool:
        return self.privilegeState

    def setPrivilegeState(self, privState: bool) -> None:
        self.privilegeState = privState 

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

    def resetSimulator(self):
        self.state = False
        self.times.setRunTime(0)
        self.times.setStopTime()

        self.metrics.setCoolantLevelPercent(100)
        self.metrics.setPowerConsumptionKWH(self.simulationMode)
        self.metrics.setLaserModulePowerWeardown(self.simulationMode)
        self.metrics.setTotalItemsProduced(0)

    def updateSimulation(self, time: datetime) -> None:
        self.times.calculateRunTime(time)
        runtime = self.times.getRuntime()
        self.metrics.updateMetrics(runtime)
        
        self.checkErrors()
        self.checkWarnings()
        
        self.ouaClient = OPCUAClient()
        logging.info("Client started")
        self.ouaClient.changeParam("Runtime", int(runtime))
        self.ouaClient.getParam()
        self.ouaClient.client.disconnect()

        self.modbusClient = ModbusTCPClient()
        logging.info("ModbusTCPClient started")
        self.modbusClient.writeSingleRegister(0, int(runtime))
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
    def getMachineStateJson(self):
        return self.getMachineState()
    
    def getProgramStateJson(self):
        return self.getProgramState()

    #return on programStateParametes in JSON format
    def getProgramState(self):
        programParameterList = [{"description": "Program runtime", "value":self.times.getRuntime()},
                           {"description": "Target amount", "value": self.metrics.getTargetAmount()},
                           {"description": "Current amount", "value": self.metrics.getTotalItemsProduced()},
                           {"description": "Coolant consumption", "value": self.metrics.getCoolantConsumption()},
                           {"description": "Power consumption", "value": self.metrics.getPowerConsumptionKWH()},
                           {"description": "Laser module power", "value": self.metrics.getLaserModulePowerWeardown()},
                           {"description": "Items per s", "value": self.metrics.getTimePerItem()},
                           ]

        data = {
            "description": "Zahnrad",
            "parameters": []
        }
        for index, param in enumerate(programParameterList):
            parameter = {
                "id": index,
                "description": param["description"],
                "value": param["value"]
            }
            data["parameters"].append(parameter)
        return data
        
    #build machineStateParameters JSON
    def getMachineState(self):
        machineParametersList = [{"description": "Runtime", "Value": self.times.getRuntime()},
                             {"description": "Coolant_level", "Value": self.metrics.getCoolantLevelPercent()},
                             {"description": "Power_consumption", "Value": self.metrics.getPowerConsumptionKWH()},
                             {"description": "Standstill_time", "Value": int(self.times.calculateIdleTime(datetime.now()))},
                             {"description": "PrivilegeState", "Value": self.getPrivilegeState()},
                             {"description": "Time_per_item", "Value": self.metrics.getTimePerItem()},
                             {"description": "Items_produced", "Value": self.metrics.getTotalItemsProduced()},
                             {"description": "Power_laser_module", "Value": self.metrics.getLaserModulePowerWeardown()},
                             ]
        
        data = {
            "parameters": []
        }

        for index, param in enumerate(machineParametersList):
            parameter = {
                "id:": index,
                "description": param["description"],
                "value": param["Value"]
            }
            data["parameters"].append(parameter)
        return data


if __name__ == "__main__":
    machine = Simulator(Triangle())
    #while True:
    for i in range(5):
        time.sleep(3)
        machine.updateSimulation(datetime.now())
    machine.resetSimulator()
    print(machine.getMachineState())
        
