from pyModbusTCP.server import ModbusServer, DataBank
from datetime import datetime
import logging
import random
import time

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')


class ModbusTCPServer:

    def __init__(self):
        self.mbS = ModbusServer(host='192.168.178.20', port=503)
        self.write_into_holding_registers(0,1)
        self.mbS.start()

    def write_into_holding_registers(self, addr, val):
        self.mbS.data_bank.set_holding_registers(addr, [1,1,1,1,1,1], srv_info=None)
        self.mbS.data_bank.set_discrete_inputs(0, [0,1,2,3,4,5])
        self.mbS.data_bank.set_input_registers(addr, [0,1,2,3,4,5])


if __name__ == '__main__':
    #data_bank = DataBank()
    ModbusTCPServer()
    