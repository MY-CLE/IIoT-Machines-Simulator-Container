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
        
        #call constructor with coolantLevelPercent and simulationMode
        self.metrics: Metrics = Metrics(100, simulationMode)
        self.warnings: Warnings = Warnings()

        #call contructor with current time to set startTime of the machine
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
        try:
            self.ouaServer = OPCUAServer()
            self.ouaServer.startServer()
            logging.info("Server started")
        except:
            self.opcuaServerThread.join()

    def startModbusServer(self):
        try:
            self.modbusServer = ModbusTCPServer()
            self.modbusServer.startServer()
            self.modbusServer.logServerChanges(0, 10)
            logging.info("Server started")
        except:
            self.modbusServerThread.join()
    
    #function to reset Simulator to default metrics, times and state
    def resetSimulator(self):
        self.state = False
        self.times.setRunTime(0)
        self.times.setStopTime()

        self.metrics.setCoolantLevelPercent(100)
        self.metrics.setPowerConsumptionKWH(self.simulationMode)
        self.metrics.setLaserModulePowerWeardown(self.simulationMode)
        self.metrics.setTotalItemsProduced(0)

    def updateSimulation(self, time: datetime) -> None:

        #calculate runtime with curret time
        self.times.calculateRunTime(time)
        runtime = self.times.getRuntime()
        #call of updateMetrics function with the runtime
        self.metrics.updateMetrics(runtime)
        
        #each time we check for errors and warnings
        self.checkErrors()
        self.checkWarnings()

        self.updateModbus()
        self.updateOPCUA()


    def updateOPCUA(self) -> None:
        try: 
            self.ouaClient = OPCUAClient()
            logging.info("OPCUA Client started")
            self.ouaClient.changeParam("Runtime", int(self.times.getRuntime()))
            self.ouaClient.changeParam("Coolant_Level", int(self.metrics.getCoolantLevelPercent()))
            self.ouaClient.changeParam("Power_Consumption", int(self.metrics.getPowerConsumptionKWH()))
            self.ouaClient.changeParam("Power_Laser", int(self.metrics.getLaserModulePowerWeardown()))
            self.ouaClient.changeParam("Idle_Time", int(self.times.getIdleTime()))
            self.ouaClient.getParam()
        except:
            self.ouaClient.client.disconnect()

    def updateModbus(self) -> None:
        try:
            self.modbusClient = ModbusTCPClient()
            logging.info("ModbusTCP Client started")
            self.modbusClient.writeSingleRegister(0, int(self.times.getRuntime()))
            self.modbusClient.writeSingleRegister(1, int(self.metrics.getCoolantLevelPercent()))
            self.modbusClient.writeSingleRegister(2, int(self.metrics.getPowerConsumptionKWH()))
            self.modbusClient.writeSingleRegister(3, int(self.metrics.getLaserModulePowerWeardown()))
            self.modbusClient.writeSingleRegister(4, int(self.times.getIdleTime()))
            self.modbusClient.readHoldingRegisters(0, 10)
        except:
            self.modbusClient.client.close()


    def checkErrors(self) -> None:
        #check if metrics are above or below a certain 'amount' to throw errors
        if self.metrics.getCoolantLevelPercent() <= 0:
            self.warnings.coolantLvlError()
            self.stopSimulator()
        if self.metrics.getPowerConsumptionKWH() >= 1000:
            self.warnings.powerConsumptionError()
            self.stopSimulator()
        if self.metrics.getLaserModulePowerWeardown() <= 0:
            self.warnings.laserModuleError()
            self.stopSimulator()

    def checkWarnings(self) -> None: 
        #check if metrics are above or below a certain 'amount' to throw warnings
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
            "description": "Triangle",
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
                             {"description": "Privilege_state", "Value": self.getPrivilegeState()},
                             {"description": "Time_per_item", "Value": self.metrics.getTimePerItem()},
                             {"description": "Items_produced", "Value": self.metrics.getTotalItemsProduced()},
                             {"description": "Power_laser_module", "Value": self.metrics.getLaserModulePowerWeardown()},
                             ]
        
        data = {
            "parameters": [],
            "error_state": {
                "errors": [],
                "warnings": [],
            }
        }

        for index, param in enumerate(machineParametersList):
            parameter = {
                "id:": str(index),
                "description": param["description"],
                "value": param["Value"]
            }
            data["parameters"].append(parameter)
        
        currentErrors = self.warnings.getErrors()
        for index, error in enumerate(currentErrors):
            tempError = {
                "id": str(index),
                "description": error
            }
            data["error_state"]["errors"].append(tempError)
            print("here")
            print(index)
            print(error)
            print(data["error_state"]["errors"])
        
        currentWarnings = self.warnings.getWarnings()
        for index, warning in enumerate(currentWarnings):
            tempWarning = {
                "id": str(index),
                "description": warning
            }
            data["error_state"]["warnings"].append(tempWarning)
        return data


if __name__ == "__main__":
    machine = Simulator(Triangle())
    #while True:
    for i in range(5):
        time.sleep(3)
        machine.updateSimulation(datetime.now())
    machine.resetSimulator()
    print(machine.getMachineState())
        
