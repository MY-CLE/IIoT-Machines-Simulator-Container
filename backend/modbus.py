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
        self.client = ModbusClient(host=os.getenv('host'), port=502, unit_id=1, auto_open=True, debug=False) # Master (Client) sendet an Slave (Server)
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
    #c.writeSingleCoil(1, True)
    i = 0
    while i < 48:
        c.writeSingleRegister(i, random.randint(0, 1500))
        """ c.writeSingleRegister(21, random.randint(0, 1500))
        c.writeSingleRegister(22, random.randint(0, 1500))
        c.writeSingleRegister(25, random.randint(0, 1500)) """
        #readInputRegisters = client.read_input_registers(0, 48) # Max reg_nb: 48
        #readHoldingRegisters  = client.read_holding_registers(0, 48) # Max reg_nb: 48
        #if readInputRegisters:
            #print(f'Read Input Registers: {readInputRegisters}')
            #print(f'Read Holding Registers: {readHoldingRegisters}')
        #else:
           #print('Read error occured')
        c.readInputRegisters(i, 1)
        """ c.readInputRegisters(21, 1)
        c.readInputRegisters(22, 1)
        c.readInputRegisters(25, 1) """
        c.readHoldingRegisters(i, 1)
        """ c.readHoldingRegisters(21, 1)
        c.readHoldingRegisters(22, 1)
        c.readHoldingRegisters(25, 1) """
        time.sleep(5)
        i = i + 1
    c.client.close()
    
