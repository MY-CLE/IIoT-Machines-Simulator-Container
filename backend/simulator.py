from datetime import datetime

import os
import time
import logging
import threading
from database.orm.machine.machineState import MachineState

from mode import Mode
from times import Times
from metrics import Metrics
from triangle import Triangle
from notifications import Warnings
from database.handler.databaseHandler import DatabaseHandler
from database.orm.program.programState import ProgramState

from opcuaIRF.opcuaServer import OPCUAServer
from opcuaIRF.opcuaClient import OPCUAClient

from modbusIRF.modbusServer import ModbusTCPServer
from modbusIRF.modbusClient import ModbusTCPClient

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')


class Simulator: 

    def __init__(self):
        self.simulatorState = False
        self.isProgramOn = False
        self.protocol = "None"
        self.privilegeState: bool = False
        self.simulationMode = Triangle()
      
        
        #call constructor with coolantLevelPercent and simulationMode
        self.metrics: Metrics = Metrics(100, self.simulationMode)
        
        self.warnings: Warnings = Warnings()

        self.times: Times = Times(datetime.now(), 0)

        
        self.opcuaServerThread = None
        self.modbusServerThread = None


    def getPrivilegeState(self) -> bool:
        return self.privilegeState

    def setPrivilegeState(self, privState: bool) -> None:
        self.privilegeState = privState 

    # if protocol is changed, stop the current server and start the new one
    def setProtocol(self, protocol: str) -> None:
        if self.protocol == protocol:
            logging.info("No protocol selected")
            return
        
        self.protocol = protocol

        if self.protocol == "Modbus/TCP" and self.opcuaServerThread != None:
            self.opcuaServerThread.join(timeout=1)
            self.opcuaServerThread = None
            logging.info("OPCUA Server stopped")

        if self.protocol == "OPCUA" and self.modbusServerThread != None:
            self.modbusServerThread.join(timeout=1)
            self.modbusServerThread = None
            logging.info("Modbus/TCP Server stopped")

        if self.protocol == "OPCUA":
            self.opcuaServerThread = threading.Thread(target=self.startOPCUAServer)
            self.opcuaServerThread.start()
        elif self.protocol == "Modbus/TCP":
            self.modbusServerThread = threading.Thread(target=self.startModbusServer)
            self.modbusServerThread.start()

    #get parameters from frontend and overwrite backend parameters
    def updateMachineStateParameters(self, data):
        attributeMapTimes = {
            'Runtime': 'RunTime',
            'Standstill_time': 'IdleTime',
        }
        attributeMapMetrics = {
            'Coolant_level': 'CoolantLevelPercent',
            'Power_consumption': 'PowerConsumptionKWH',
            'Time_per_item': 'TimePerItem',
            'Items_produced': 'TotalItemsProduced',
            'Power_laser_module': 'LaserModulePowerWeardown'
        }

        for key, value in data.items():
            if key == 'value':
                description = data.get('description')
                if description in attributeMapTimes:
                    attribute = attributeMapTimes.get(description)
                    setMethod = getattr(self.times, 'set' + attribute)
                    setMethod(value)
                elif description in attributeMapMetrics:
                    attribute = attributeMapMetrics.get(description)
                    setMethod = getattr(self.metrics, 'set' + attribute)
                    setMethod(value)

    def setMode(self, modeId: str) -> None:
        self.simulationMode = DatabaseHandler().selectMachineProgramById(modeId)

    def stopSimulator(self) -> None:
        self.simulatorState = False
    
    def startSimulator(self) -> None:
        self.simulatorState = True
    
    def startProgram(self) -> None:
        self.isProgramOn = True
        self.times.setStartTime(datetime.now())

    def stopProgram(self) -> None:
        self.isProgramOn = False
        self.times.setStopTime()
        logging.info("Machine stopped!")

    def startOPCUAServer(self):
        self.ouaServer = OPCUAServer()
        self.ouaServer.startServer()
        logging.info("Server started")

    def startModbusServer(self):
        self.modbusServer = ModbusTCPServer()
        self.modbusServer.startServer()
        self.modbusServer.logServerChanges(0, 10)
        logging.info("Server started")
    
    #function to reset Simulator to default metrics, times and simulatorState
    def resetSimulator(self):
        self.simulatorState = False
        self.times.setRunTime(0)
        self.times.setStopTime()
        self.times.setIdleTime(0)
        #state of times to be set True so idleTime stops counting
        self.times.setState(True)

        self.metrics.setCoolantLevelPercent(100)
        self.metrics.setPowerConsumptionKWHMode(self.simulationMode)
        self.metrics.setLaserModulePowerWeardownMode(self.simulationMode)
        self.metrics.setTotalItemsProduced(0)

    def updateSimulation(self, time: datetime) -> None:
        if(self.isProgramOn == True):
            #calculate runtime with curret time
            self.times.calculateRunTime(time)
            runtime = self.times.getRuntime()
            #call of updateMetrics function with the runtime
            self.metrics.updateMetrics(runtime)
            
            #each time we check for errors and warnings
            self.checkErrors()
            self.checkWarnings()
            if(self.protocol == "Modbus/TCP"):
                self.updateModbus()
            if(self.protocol == "OPCUA"):
                self.updateOPCUA()

    # implemenation of OPCUA into the simulator
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

    # implemenation of Modbus into the simulator
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
    
    def getPrograms(self):
        return DatabaseHandler.selectAllMachinePrograms()
    
    #here is TotalItemsProduced implemeted instead CurrentAmount
    def saveSimulation(self, simName: str ):
        activeProgram = 1#self.simulationMode.getProgramId()
        programState = ProgramState(0,activeProgram, self.metrics.getTargetAmount(), self.metrics.getTotalItemsProduced(), self.times.getRuntime())
        stateId = DatabaseHandler.storeProgramState(programState)
        machineState = MachineState(0, simName, 0, 0, stateId, self.times.getStartTime(), self.times.getStopTime(), self.times.getIdleTime(), self.metrics.getTotalItemsProduced(), self.metrics.getPowerConsumptionKWH(), self.metrics.getLaserModulePowerWeardown(),self.metrics.getCoolantLevelPercent())
        DatabaseHandler.storeMachineState(machineState)

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
            "description": self.simulationMode.getDescription(),
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
                "name": error
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
                "name": warning
            }
            data["error_state"]["warnings"].append(tempWarning)
        return data


""" if __name__ == "__main__":
    machine = Simulator(Triangle())
    #while True:
    for i in range(5):
        time.sleep(3)
        machine.updateSimulation(datetime.now())
    machine.resetSimulator()
    print(machine.getMachineState())
        
 """