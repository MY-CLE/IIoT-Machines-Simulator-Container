import logging
import threading

from datetime import datetime

from logic.machine import Machine
from logic.program import Program
from logic.notifications import Notifications
from database.handler.databaseHandler import DatabaseHandler

from opcuaIRF.opcuaServer import OPCUAServer
from opcuaIRF.opcuaClient import OPCUAClient

from modbusIRF.modbusServer import ModbusTCPServer
from modbusIRF.modbusClient import ModbusTCPClient

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s',
                    level=logging.INFO, encoding='utf-8')


class Simulator:

    def __init__(self):
        self.simulatorState = False
        self.protocol = "None"
        self.privilegeState: bool = False
        self.simulatedProgram: Program = Program()
        self.simulatedMachine: Machine = Machine()
        self.notification: Notifications = Notifications()

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

        if self.protocol != "Modbus/TCP" and self.modbusServerThread != None:
            self.modbusServerThread.join(timeout=1)
            self.modbusServerThread = None
            logging.info("Modbus/TCP Server stopped")

        if self.protocol != "OPCUA" and self.opcuaServerThread != None:
            self.opcuaServerThread.join(timeout=1)
            self.opcuaServerThread = None
            logging.info("OPCUA Server stopped")

        if self.protocol == "OPCUA":
            self.opcuaServerThread = threading.Thread(
                target=self.startOPCUAServer)
            self.opcuaServerThread.daemon = True
            self.opcuaServerThread.start()
        elif self.protocol == "Modbus/TCP":
            self.modbusServerThread = threading.Thread(
                target=self.startModbusServer)
            self.modbusServerThread.daemon = True
            self.modbusServerThread.start()

    def updateProgramParameters(self, data):
        self.simulatedProgram.setProgramParameters()

    # get parameters from frontend and overwrite backend parameters
    def updateMachineStateParameters(self, data):
        machineAttributesMap = {
            'Runtime (s)': 'MachineRuntime',
            'Idle Time (s)': 'MachineIdleTime',
            'Coolant Level (%)': 'CoolantLevel',
            'Power Consumption (Wh)': 'TotalEnegeryConsumption',
            'Capacity Laser Module (%)': 'CapacityLaserModule',
            'Total Items': 'TotalItems'
        }
        programAttributeMap = {
            'Program Runtime (s)': 'ProgramRuntime',
            'Target Amount': 'ProgramTargetAmount',
            'Current Amount': 'ProgramCurrentAmount',
            'Coolant Consumption (% / s)': 'ProgramCoolantConsumption',
            'Laser Module Weardown (% / s)': 'ProgramLaserModuleWeardown',
            'Laser Power Consumption (W)': 'ProgramLaserModulePowerConsumption',
            'Time per Item (s)': 'ProgramTimePerItem'
        }

        for key, value in data.items():
            if key == 'value':
                description = data.get('description')
                if description in machineAttributesMap:
                    attribute = machineAttributesMap.get(description)
                    setMethod = getattr(
                        self.simulatedMachine, 'set' + attribute)
                    setMethod(value)
                elif description in programAttributeMap:
                    attribute = programAttributeMap.get(description)
                    setMethod = getattr(
                        self.simulatedProgram, 'set' + attribute)
                    setMethod(value)

    def stopMachine(self) -> None:
        date = datetime.now()
        self.simulatorState = False
        self.stopProgram()
        self.simulatedMachine.stopMachine(date)

    def startMachine(self) -> None:
        self.resetSimulator()
        self.simulatedProgram.resetToDefaultState()
        self.simulatorState = True
        self.simulatedMachine.startMachine(datetime.now())

    # function to start machine with parameters loaded from database
    def loadMachine(self) -> None:
        self.simulatorState = True
        self.simulatedMachine.startMachine(datetime.now())

    def startProgram(self) -> None:
        date = datetime.now()
        self.simulatedProgram.startProgram(date)
        self.simulatedMachine.setIsProgramRunning(True)

    def stopProgram(self) -> None:
        date = datetime.now()
        self.simulatedProgram.stopProgram(date)
        # needed to calculate idleTime cos idleTime is machine parameter
        self.simulatedMachine.setMachineStopTime(date)
        self.simulatedMachine.setIsProgramRunning(False)
        logging.info("Machine stopped!")

    def startOPCUAServer(self):
        self.ouaServer = OPCUAServer()
        self.ouaServer.startServer()

    def startModbusServer(self):
        self.modbusServer = ModbusTCPServer()
        self.modbusServer.startServer()
        self.modbusServer.logServerChanges(0, 10)

    # function to reset Simulator to default metrics, times and simulatorState
    def resetSimulator(self):
        self.simulatedMachine.resetMachine()
        self.simulatedProgram.resetProgram()

    def updateSimulation(self, time: datetime) -> None:
        self.simulatedMachine.updateMachineErrors(
            self.notification.getErrors(), self.notification.getWarnings())
        self.checkErrors()
        self.checkWarnings()
        if(self.protocol == "Modbus/TCP"):
            self.updateModbus()
        if(self.protocol == "OPCUA"):
            self.updateOPCUA()
        if(self.simulatedMachine.isProgramRunning):
            self.checkErrors()
            self.checkWarnings()
            # calculate runtime with curret time
            # self.times.calculateRunTime(time)
            updatedParameter: list = self.simulatedProgram.updateProgram(time)
            machineRuntime = self.simulatedMachine.updateMachine(
                time, *updatedParameter)
            self.simulatedProgram.checkMachineRuntimeValue(machineRuntime)

        # if clause to check wether or not idleTime needs to be calculated
        else:
            self.simulatedMachine.calculateIdleTime(time)

    # implemenation of OPCUA into the simulator
    def updateOPCUA(self) -> None:
        try:
            self.ouaClient = OPCUAClient()
            logging.info("OPCUA Client started")
            self.ouaClient.changeParam("Runtime", int(
                self.simulatedMachine.getMachineRuntime()))
            self.ouaClient.changeParam("Idle_Time", int(
                self.simulatedMachine.getMachineIdleTime()))
            self.ouaClient.changeParam("Coolant_Level", int(
                self.simulatedMachine.getCoolantLevel()))
            self.ouaClient.changeParam("Power_Consumption", int(
                self.simulatedMachine.getTotalEnegeryConsumption()/1000))  # in kWh
            self.ouaClient.changeParam("Capacity_Laser_Module", int(
                self.simulatedMachine.getCapacityLaserModule()))
            self.ouaClient.changeParam("Total_Items", int(
                self.simulatedMachine.getTotalItems()))

            self.ouaClient.getParam()

            if(self.simulatedMachine.isProgramRunning):
                self.ouaClient.changeParam("Program_Runtime", int(
                    self.simulatedProgram.getProgramRuntime()))
                self.ouaClient.changeParam("Target_Amount", int(
                    self.simulatedProgram.getProgramTargetAmount()))
                self.ouaClient.changeParam("Current_Amount", int(
                    self.simulatedProgram.getProgramCurrentAmount()))
                self.ouaClient.changeParam("Coolant_Consumption", int(
                    self.simulatedProgram.getProgramCoolantConsumption()*100))
                self.ouaClient.changeParam("Laser_Module_Weardown", int(
                    self.simulatedProgram.getProgramLaserModuleWeardown()*100))
                self.ouaClient.changeParam("Laser_Power_Consumption", int(
                    self.simulatedProgram.getProgramLaserModulePowerConsumption()))
                self.ouaClient.changeParam("Time_Per_Item", int(
                    self.simulatedProgram.getProgramTimePerItem()))

                self.ouaClient.getParam()
        except:
            self.ouaClient.client.disconnect()

    # implemenation of Modbus into the simulator
    def updateModbus(self) -> None:
        try:
            self.modbusClient = ModbusTCPClient()
            logging.info("ModbusTCP Client started")
            self.modbusClient.writeSingleRegister(
                0, int(self.simulatedMachine.getMachineRuntime()))
            self.modbusClient.writeSingleRegister(
                1, int(self.simulatedMachine.getMachineIdleTime()))
            self.modbusClient.writeSingleRegister(
                2, int(self.simulatedMachine.getCoolantLevel()))
            self.modbusClient.writeSingleRegister(
                3, int(self.simulatedMachine.getTotalEnegeryConsumption()/1000))  # in kWh
            self.modbusClient.writeSingleRegister(
                4, int(self.simulatedMachine.getCapacityLaserModule()))
            self.modbusClient.writeSingleRegister(
                5, int(self.simulatedMachine.getTotalItems()))

            self.modbusClient.readHoldingRegisters(0, 6)

            if(self.simulatedMachine.isProgramRunning):
                self.modbusClient.writeSingleRegister(
                    6, int(self.simulatedProgram.getProgramRuntime()))
                self.modbusClient.writeSingleRegister(
                    7, int(self.simulatedProgram.getProgramTargetAmount()))
                self.modbusClient.writeSingleRegister(
                    8, int(self.simulatedProgram.getProgramCurrentAmount()))
                self.modbusClient.writeSingleRegister(
                    9, int(self.simulatedProgram.getProgramCoolantConsumption()*100))
                self.modbusClient.writeSingleRegister(
                    10, int(self.simulatedProgram.getProgramLaserModuleWeardown()*100))
                self.modbusClient.writeSingleRegister(
                    11, int(self.simulatedProgram.getProgramLaserModulePowerConsumption()))
                self.modbusClient.writeSingleRegister(
                    12, int(self.simulatedProgram.getProgramTimePerItem()))

                self.modbusClient.readHoldingRegisters(6, 7)
        except:
            self.modbusClient.client.close()

    def checkErrors(self) -> None:
        # check if metrics are above or below a certain 'amount' to throw errors
        if self.simulatedMachine.getCoolantLevel() <= 5:
            self.warnings.coolantLvlError()
            self.stopMachine()
        if self.simulatedMachine.getCapacityLaserModule() <= 5:
            self.warnings.laserModuleError()
            self.stopMachine()

    def checkWarnings(self) -> None:
        # check if metrics are above or below a certain 'amount' to throw warnings
        if self.simulatedMachine.getCoolantLevel() <= 10:
            self.warnings.coolantLvlWarning()
        if self.simulatedMachine.getTotalEnegeryConsumption() >= 90000000:
            self.warnings.powerConsumptionWarning()
        if self.simulatedMachine.getCapacityLaserModule() <= 10:
            self.warnings.laserModuleWarning()

    def getPrograms(self):
        return DatabaseHandler.selectAllMachinePrograms()

    # here is TotalItemsProduced implemeted instead CurrentAmount
    def saveSimulation(self, simName: str) -> None:
        #raise Exception(self.protocol)
        stateId = DatabaseHandler.storeProgramState(
            self.simulatedProgram.getAsProgramState())
        protocol = DatabaseHandler.selectProtocolByName(self.protocol)
        self.simulatedMachine.prepareForDB(
            datetime.now(), simName, protocol.getProtocolID(), stateId)
        DatabaseHandler.storeMachineState(
            self.simulatedMachine.getAsMachineState())

    def loadSimulation(self, simulationId) -> None:
        machineState = DatabaseHandler.selectMachineState(simulationId)
        programState = DatabaseHandler.selectProgramState(
            machineState.getProgramState())
        self.protocol = DatabaseHandler.selectProtocolById(
            machineState.getMachineProtocol()).getProtocolDescription()
        self.simulatedMachine.loadMachineState(machineState)
        self.simulatedProgram.loadProgramState(programState)
        self.loadMachine()

    def loadSimulationById(self, simulationId) -> dict:
        machineState = DatabaseHandler.selectMachineState(simulationId)
        programState = DatabaseHandler.selectProgramState(
            machineState.getProgramState())

        return {
            "simulation": {
                "id": machineState.getId(),
                "machineState": machineState.getJson(),
                "programState": programState.getJson(),
            },
        }

    def deleteSimulationById(self, simulationId) -> None:
        DatabaseHandler.deleteMachineStateById(simulationId)