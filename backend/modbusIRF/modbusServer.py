from pyModbusTCP.server import ModbusServer

import time
import socket
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')

def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class ModbusTCPServer:

    def __init__(self):
        self.mbS = ModbusServer(host=getIPAddress(), port=504, no_block=True) # Initialize Modbus Server with IP and Port
        self.mbS.data_bank.set_holding_registers(address=0, word_list=[], srv_info=None) # Set Holding Register can be changed by the client
        """ self.mbS.data_bank.set_coils(address=0, bit_list=[], srv_info=None) # Set Coils can be changed by the client """

    def startServer(self): # Start the server and log the status
        try:
            self.mbS.start()
            logging.info("Server is running")
        except:
            logging.error("Server is shutting down")
            self.mbS.stop()
            logging.error("Server is stopped")

    def logServerChanges(self, regAddr: int = 0, numParams: int = 1): # Log changes of the registers

        logging.info("Logging changes of the registers")

        previousState = self.mbS.data_bank.get_holding_registers(address=regAddr, number=numParams)  # Get initial state of all registers

        while True:
            currentState = self.mbS.data_bank.get_holding_registers(address=regAddr, number=numParams)
            for addr, prevValue, currValue in zip(range(len(previousState)), previousState, currentState): # Tripel of addr, prevValue, currValue
                if prevValue != currValue:
                    logging.info(f"Register {addr} changed: {prevValue} -> {currValue}")
            previousState = currentState
            time.sleep(0.5)

""" if __name__ == '__main__':
    server = ModbusTCPServer()
    server.startServer()
    server.logServerChanges(0, 10) """
