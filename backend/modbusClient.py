from pyModbusTCP.client import ModbusClient
from dotenv import load_dotenv

import os
import time
import random
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')

load_dotenv()

class Modbus:
    connError = 'Connection couldn\'t be established - Check host ip-address & port number'

    def __init__(self):
        self.client = ModbusClient(host='192.168.178.20', port=504, unit_id=3, auto_open=True, debug=False) # Master (Client) sendet an Slave (Server)
        self.connEstablished = self.client.open()
        if self.connEstablished:
            logging.info(f'Connection established: {self.connEstablished}')
        else:
            logging.error(self.connError)

    def writeSingleRegister(self, regAddr: int = 0, regValue: int = 0):
        if self.connEstablished:
            wSR = self.client.write_single_register(regAddr, regValue)
            logging.info(f'Write Single Register | Writing at register Address: {regAddr} --> {regValue}')
            return wSR
        else:
            logging.error(self.connError)

    def writeSingleCoil(self, bitAddr, bitValue):
        if self.connEstablished:
            wSC = self.client.write_single_coil(bitAddr, bitValue)
            logging.info(f'Write Single Coil | Writing at Coil Address: {bitAddr} --> {bitValue}')
            return wSC
        else:
            logging.error(self.connError)

    def writeMultipleRegisters(self, regAddr: int = 0, regValue: int = 0):
        if self.connEstablished:
            wMR = self.client.write_multiple_registers(regAddr, regValue)
            logging.info(f'Write Single Register | Writing at register Address: {regAddr} --> {regValue}')
            return  wMR
        else:
            logging.error(self.connError)
    
    def readInputRegisters(self, regAddr: int = 0, count: int = 1):
        if self.connEstablished:
            rIR = self.client.read_input_registers(regAddr, count)
            logging.info(f'Read Input Registers | Start reading at Address: {regAddr} until {regAddr-1+count} --> {rIR}')
            return rIR
        else:
            logging.error(self.connError)

    def readHoldingRegisters(self, regAddr: int = 0, count: int = 1):
        if self.connEstablished:
            rHR = self.client.read_holding_registers(regAddr, count)
            logging.info(f'Read Holding Registers | Start reading at Address: {regAddr} --> {rHR}')
            return rHR
        else:
            logging.error(self.connError)

if __name__ == '__main__':
    c = Modbus()
    i = 0
    while i < 10:
        #c.writeMultipleRegisters(0,[2222,3222])
        c.writeSingleRegister(i, random.randint(0, 65535))
        c.readHoldingRegisters(0, 10)

        #c.readHoldingRegisters(i, 10)

        time.sleep(0.5)
        i = i + 1
        if i == 9:
            i = 0
    c.client.close()
    
