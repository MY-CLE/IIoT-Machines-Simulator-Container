from pyModbusTCP.server import ModbusServer, DataBank
from datetime import datetime
import logging
import random
import time

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')


class ModbusTCPServer:

    def __init__(self):
        self.mbS = ModbusServer(host='192.168.178.20', port=504, no_block=True)

    def write_into_registers(self, addr, val):
        self.mbS.data_bank.set_holding_registers(address=addr, word_list=[], srv_info=None) # Holding Register cannot be accessed by the client they have fixed values
        #self.mbS.data_bank.set_discrete_inputs(0, [0,1,2,3,4,5])
        #self.mbS.data_bank.set_input_registers(addr, [0,0,0,0,0,0,0,0]) # Input Register can be changed by the client


if __name__ == '__main__':
    try:
        server = ModbusTCPServer()
        server.mbS.start()
        logging.info("Server is running")
        state = [0]
        while True:
            server.write_into_registers(0,1)
            if state != server.mbS.data_bank.get_holding_registers(1):
                logging.info(f"State: {state}")
                state = server.mbS.data_bank.get_holding_registers(1)
                logging.info(f"State: {state}")
                time.sleep(0.5)

    except:
        logging.error("Server is shutting down")
        server.mbS.stop()
        logging.error("Server is stopped")