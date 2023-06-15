from pyModbusTCP.client import ModbusClient

import socket
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')

# Get the IP Address of the machine
def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# Modbus TCP Client
# Master (Client) sends data to Slave (Server) and receives data from Slave
class ModbusTCPClient:
    connError = 'Connection couldn\'t be established - Check host ip-address & port number'

    def __init__(self) -> None:
        self.client = ModbusClient(host=getIPAddress(), port=504, unit_id=3, auto_open=True, debug=False)
        self.connEstablished = self.client.open()
        if self.connEstablished:
            logging.info(f'Connection established: {self.connEstablished}')
        else:
            logging.error(self.connError)

    # Write into a single register (16 bit) at a given address
    def writeSingleRegister(self, regAddr: int = 0, regValue: int = 0) -> None:
        if self.connEstablished:
            wSR = self.client.write_single_register(regAddr, regValue)
            logging.info(f'Write Single Register\t| Writing at register Address {regAddr} --> {regValue}')
            return wSR
        else:
            logging.error(self.connError)

    # Write into a single coil (1 bit) at a given address | NOT USED IN THIS PROJECT because IRF doesn't support it yet
    def writeSingleCoil(self, bitAddr: int = 0, bitValue: int = 0) -> None:
        if self.connEstablished:
            wSC = self.client.write_single_coil(bitAddr, bitValue)
            logging.info(f'Write Single Coil\t| Writing at bit Address: {bitAddr} --> {bitValue}')
            return wSC
        else:
            logging.error(self.connError)

    # Write into multiple registers (16 bit) at a given address
    def writeMultipleRegisters(self, regAddr: int = 0, regValue: int = 0) -> None:
        if self.connEstablished:
            wMR = self.client.write_multiple_registers(regAddr, regValue)
            logging.info(f'Write Multiple Registers\t| Writing at register Address: {regAddr} --> {regValue}')
            return  wMR
        else:
            logging.error(self.connError)

    # Write into multiple coils (1 bit) at a given address | NOT USED IN THIS PROJECT because IRF doesn't support it yet
    def writeMultipleCoils(self, bitAddr: int = 0, bitValue: int = 0) -> None:
        if self.connEstablished:
            wMR = self.client.write_multiple_coils(bitAddr, bitValue)
            logging.info(f'Write Multiple Coils\t| Writing at bit Address: {bitAddr} --> {bitValue}')
            return  wMR
        else:
            logging.error(self.connError)
    
    # Read from input registers (each 16 bit) at a given address for a given range of addresses 
    def readInputRegisters(self, regAddr: int = 0, count: int = 1) -> None:
        if self.connEstablished:
            rIR = self.client.read_input_registers(regAddr, count)
            logging.info(f'Read Input Registers\t| Start reading at register Address: {regAddr} until {regAddr-1+count} --> {rIR}')
            return rIR
        else:
            logging.error(self.connError)

    # Read from holding registers (each 16 bit) at a given address for a given range of addresses
    def readHoldingRegisters(self, regAddr: int = 0, count: int = 1) -> None:
        if self.connEstablished:
            rHR = self.client.read_holding_registers(regAddr, count)
            logging.info(f'Read Holding Registers\t| Start reading at register Address: {regAddr} --> {rHR}')
            return rHR
        else:
            logging.error(self.connError)

    # Read from input coils (each 1 bit) at a given address for a given range of addresses | NOT USED IN THIS PROJECT because IRF doesn't support it yet
    def readCoils(self, bitAddr: int = 0, count: int = 1) -> None:
        if self.connEstablished:
            rHR = self.client.read_coils(bitAddr, count)
            logging.info(f'Read Coils\t\t| Start reading at bit Address: {bitAddr} --> {rHR}')
            return rHR
        else:
            logging.error(self.connError)