from datetime import datetime

import os
import time
import logging
import threading
from database.orm.machine.machineState import MachineState

from machine import Machine
from program import Program
from mode import Mode
from times import Times
from metrics import Metrics
from triangle import Triangle
from rectangle import Rectangle
from circle import Circle
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
        self.protocol = "None"
        self.privilegeState: bool = False
        self.simulatedProgram: Program = Program()
        self.simulatedMachine: Machine = Machine()	
        self.warnings: Warnings = Warnings()
        
        self.opcuaServerThread = None
        self.modbusServerThread = None


    def getPrivilegeState(self) -> bool:
        return self.privilegeState

    def setPrivilegeState(self, privState: bool) -> None:
        self.privilegeState = privState 

    # if protocol is changed, stop the current server and start the new one
    def setProtocol(self, protocol: str) -> None:
        if self.protocol == protocol:
            logging.info(f"Protocol '{self.protocol}' already selected")
            return
        
        self.protocol = protocol

        if (self.protocol == "Modbus/TCP" or self.protocol == "None") and self.opcuaServerThread != None:
            self.opcuaServerThread.join(timeout=1)
            self.opcuaServerThread = None
            logging.info("OPCUA Server stopped")

        if (self.protocol == "OPCUA" or self.protocol == "None") and self.modbusServerThread != None:
            self.modbusServerThread.join(timeout=1)
            self.modbusServerThread = None
            logging.info("Modbus/TCP Server stopped")

        if self.protocol == "OPCUA":
            self.opcuaServerThread = threading.Thread(target=self.startOPCUAServer)
            self.opcuaServerThread.start()
        elif self.protocol == "Modbus/TCP":
            self.modbusServerThread = threading.Thread(target=self.startModbusServer)
            self.modbusServerThread.start()

    def updateProgramParameters(self, data):
        self.simulatedProgram.setProgramParameters()

    #get parameters from frontend and overwrite backend parameters
    def updateMachineStateParameters(self, data):
        machineAttributesMap = {
            'RunTime': 'MachineRuntime',
            'Machine Idle Time': 'MachineIdleTime',
            'Coolant level': 'CoolantLevel',
            'Power Consumption': 'TotalEnegeryConsumption',
            'Capacity Laser Module': 'CapacityLaserModule',
            'Total Items': 'TotalItems'
        }
        programAttributeMap = {
            'Program runtime': 'ProgramRuntime',
            'Target amount': 'ProgramTargetAmount',
            'Current Amount': 'ProgramCurrentAmount',
            'Coolant consumption per s': 'ProgramCoolantConsumption',
            'Laser Module Wear Down': 'ProgramLaserModuleWeardown',
            'Laser Power Consumption': 'ProgramLaserModulePowerConsumption',
            'Sec per Item': 'ProgramTimePerItem'
        }

        for key, value in data.items():
            if key == 'value':
                description = data.get('description')
                if description in machineAttributesMap:
                    attribute = machineAttributesMap.get(description)
                    setMethod = getattr(self.simulatedMachine, 'set' + attribute)
                    setMethod(value)
                elif description in programAttributeMap:
                    attribute = programAttributeMap.get(description)
                    setMethod = getattr(self.simulatedProgram, 'set' + attribute)
                    setMethod(value)

    def stopSimulator(self) -> None:
        self.simulatorState = False
    
    def startMachine(self) -> None:
        self.simulatorState = True
        self.simulatedMachine.startMachine(datetime.now())
    
    def startProgram(self) -> None:
        date = datetime.now()
        self.simulatedProgram.startProgram(date) 
        self.simulatedMachine.setIsProgramRunning(True)

    def stopProgram(self) -> None:
        self.simulatedProgram.setIsProgramRunning(False)
        self.simulatedMachine.setIsProgramRunning(False)
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
        self.simulatedMachine.resetMachine()
        self.simulatedProgram.resetProgram()

    def updateSimulation(self, time: datetime) -> None:        
        if(self.simulatedMachine.isProgramRunning):
            #calculate runtime with curret time
            #self.times.calculateRunTime(time)
            self.simulatedMachine.updateMachineErrors(self.warnings.getErrors(), self.warnings.getWarnings())
            updatedParameter:list = self.simulatedProgram.updateProgram(time)
            self.simulatedMachine.updateMachine(time, *updatedParameter)

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
        if self.simulatedMachine.getCoolantLevel() <= 0:
            self.warnings.coolantLvlError()
            self.stopSimulator()
        if self.simulatedMachine.getTotalEnegeryConsumption() >= 100000:
            self.warnings.powerConsumptionError()
            self.stopSimulator()
        if self.simulatedProgram.getProgramLaserModulePowerConsumption() <= 1000:
            self.warnings.laserModuleError()
            self.stopSimulator()

    def checkWarnings(self) -> None: 
        #check if metrics are above or below a certain 'amount' to throw warnings
        if self.simulatedMachine.getCoolantLevel() <= 10:
            self.warnings.coolantLvlWarning()
        if self.simulatedMachine.getTotalEnegeryConsumption() >= 90000:
            self.warnings.powerConsumptionWarning()
        if self.simulatedProgram.getProgramLaserModulePowerConsumption() <= 1200:
            self.warnings.laserModuleWarning()
   
    def getPrograms(self):
        return DatabaseHandler.selectAllMachinePrograms()
    
    #here is TotalItemsProduced implemeted instead CurrentAmount
    def saveSimulation(self, simName: str ):
        stateId = DatabaseHandler.storeProgramState(self.simulatedProgram.getAsProgramState())
        protocol = DatabaseHandler.selectProtocolByName(self.protocol)
        self.simulatedMachine.prepareForDB(datetime.now(), simName, protocol.getProtocolID(), stateId)
        DatabaseHandler.storeMachineState(self.simulatedMachine.getAsMachineState())
        
    def loadSimulation(self, simulation_id):
        machineState = DatabaseHandler.selectMachineState(simulation_id)
        programState = DatabaseHandler.selectProgramState(machineState.getProgramState())
        self.protocol = DatabaseHandler.selectProtocolById(machineState.getMachineProtocol()).getProtocolDescription()
        self.simulatedMachine.loadMachineState(machineState)
        self.simulatedProgram.loadProgramState(programState)
        self.startMachine()
