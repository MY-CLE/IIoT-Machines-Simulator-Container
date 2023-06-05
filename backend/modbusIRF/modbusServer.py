from pyModbusTCP.server import ModbusServer

import time
import socket
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')

# Get the IP Address of the machine
def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# Modbus TCP Server
# Slave (Server) receives data from Master (Client) and can either send data back or change its own data
class ModbusTCPServer:

    def __init__(self) -> None:
        self.mbS = ModbusServer(host=getIPAddress(), port=504, no_block=True) # Initialize Modbus Server with IP and Port
        self.mbS.data_bank.set_holding_registers(address=0, word_list=[], srv_info=None) # Set Holding Register can be changed by the client
        #self.mbS.data_bank.set_coils(address=0, bit_list=[], srv_info=None) # Set Coils can be changed by the client | NOT USED IN THIS PROJECT because IRF doesn't support it yet

    # Start the server and log the status
    def startServer(self) -> None:
        try:
            self.mbS.start()
            logging.info("ModbusTCP Server started")
        except:
            logging.error("ModbusTCP Server is shutting down")
            self.mbS.stop()
            logging.error("ModbusTCP Server is stopped")

    # Log changes of the holding registers (16 bit) at a given address for a given range of addresses 
    def logServerChanges(self, regAddr: int = 0, numParams: int = 1) -> None:

        logging.info("Logging changes of the registers")

        previousState = self.mbS.data_bank.get_holding_registers(address=regAddr, number=numParams)  # Get initial state of all registers

        while True:
            currentState = self.mbS.data_bank.get_holding_registers(address=regAddr, number=numParams) # Get current state of all registers
            for addr, prevValue, currValue in zip(range(len(previousState)), previousState, currentState): # Tripel of addr, prevValue, currValue
                if prevValue != currValue:
                    logging.info(f"Register {addr} changed: {prevValue} -> {currValue}") 
            previousState = currentState
            time.sleep(0.5)