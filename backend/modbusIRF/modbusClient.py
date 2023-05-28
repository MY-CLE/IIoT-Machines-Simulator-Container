from pyModbusTCP.client import ModbusClient

import time
import socket
import random
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')

def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class ModbusTCPClient:
    connError = 'Connection couldn\'t be established - Check host ip-address & port number'

    def __init__(self):
        self.client = ModbusClient(host=getIPAddress(), port=504, unit_id=3, auto_open=True, debug=False) # Master (Client) sends data to Slave (Server)
        self.connEstablished = self.client.open()
        if self.connEstablished:
            logging.info(f'Connection established: {self.connEstablished}')
        else:
            logging.error(self.connError)

    def writeSingleRegister(self, regAddr: int = 0, regValue: int = 0):
        if self.connEstablished:
            wSR = self.client.write_single_register(regAddr, regValue)
            logging.info(f'Write Single Register\t| Writing at register Address {regAddr} --> {regValue}')
            return wSR
        else:
            logging.error(self.connError)

    def writeSingleCoil(self, bitAddr, bitValue):
        if self.connEstablished:
            wSC = self.client.write_single_coil(bitAddr, bitValue)
            logging.info(f'Write Single Coil\t| Writing at bit Address: {bitAddr} --> {bitValue}')
            return wSC
        else:
            logging.error(self.connError)

    def writeMultipleRegisters(self, regAddr: int = 0, regValue: int = 0):
        if self.connEstablished:
            wMR = self.client.write_multiple_registers(regAddr, regValue)
            logging.info(f'Write Multiple Registers\t| Writing at register Address: {regAddr} --> {regValue}')
            return  wMR
        else:
            logging.error(self.connError)
    
    def writeMultipleCoils(self, bitAddr: int = 0, bitValue: int = 0):
        if self.connEstablished:
            wMR = self.client.write_multiple_coils(bitAddr, bitValue)
            logging.info(f'Write Multiple Coils\t| Writing at bit Address: {bitAddr} --> {bitValue}')
            return  wMR
        else:
            logging.error(self.connError)
    
    def readInputRegisters(self, regAddr: int = 0, count: int = 1):
        if self.connEstablished:
            rIR = self.client.read_input_registers(regAddr, count)
            logging.info(f'Read Input Registers\t| Start reading at register Address: {regAddr} until {regAddr-1+count} --> {rIR}')
            return rIR
        else:
            logging.error(self.connError)

    def readHoldingRegisters(self, regAddr: int = 0, count: int = 1):
        if self.connEstablished:
            rHR = self.client.read_holding_registers(regAddr, count)
            logging.info(f'Read Holding Registers\t| Start reading at register Address: {regAddr} --> {rHR}')
            return rHR
        else:
            logging.error(self.connError)

    def readCoils(self, bitAddr: int = 0, count: int = 1):
        if self.connEstablished:
            rHR = self.client.read_coils(bitAddr, count)
            logging.info(f'Read Coils\t\t| Start reading at bit Address: {bitAddr} --> {rHR}')
            return rHR
        else:
            logging.error(self.connError)

""" if __name__ == '__main__':
    c = ModbusTCPClient()
    #c.writeSingleCoil(0, True)
    i = 0
    while i < 10:

        c.writeSingleRegister(i, random.randint(0, 65535))
        c.readHoldingRegisters(0, 10)
        #c.readCoils(0, 2)

        time.sleep(0.5)
        i+=1
        if i == 9:
            i=0
    c.client.close()
     """
