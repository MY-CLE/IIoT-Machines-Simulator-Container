from pymodbus.client import ModbusTcpClient

import random
import time
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.DEBUG, encoding='utf-8')

client = ModbusTcpClient(host="192.168.178.60", port=502, debug=True) # Master sendet an Slave
logging.info(f'Connection established: {client.connect()}')
client.write_coil(0x01, True)

client.read_coils(0x01)
result = client.read_input_registers(64)
print(result)
client.close()