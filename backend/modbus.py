from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="192.168.178.60", port=502, debug=True) # Master sendet an Slave
client.open()
print(client.read_holding_registers(0,4))