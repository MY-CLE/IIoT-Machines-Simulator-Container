from opcua import Client

import socket
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')
logging.getLogger("opcua").setLevel(logging.WARNING)

# Get the IP Address of the machine
def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# OPC-UA Client
# Client reads and writes the parameters from the server
class OPCUAClient:

    def __init__(self):
        self.client = Client(f"opc.tcp://{getIPAddress()}:4840")
        self.client.connect()
        self.data_variables = ["Runtime", "Idle_Time", "Coolant_Level", "Power_Consumption", "Capacity_Laser_Module", "Total_Items", "Program_Runtime", "Target_Amount", "Current_Amount", "Coolant_Consumption", "Laser_Module_Weardown", "Laser_Power_Consumption", "Time_Per_Item"]
        self.nameIndex = self.client.get_namespace_index("MOUSP") # namespace Machinesimulator OPC-UA Server Parameter - Index = 2
        self.node = self.client.get_root_node()

    # Get the parameters from the server and loop through the variables to get the values and log them
    def getParam(self):
        for i in range(len(self.data_variables)):
            self.param = self.node.get_child(["0:Objects", f"{self.nameIndex}:Parameters", f"{self.nameIndex}:{self.data_variables[i]}"])
            self.infoParam = str(self.param.nodeid) + " - " + self.param.get_browse_name().Name + ": " + str(self.param.get_value())
            logging.info(self.infoParam)
            print("test")

    # Change the parameters on the server
    def changeParam(self, param, value):
        self.newParam = self.node.get_child(["0:Objects", f"{self.nameIndex}:Parameters", f"{self.nameIndex}:{param}"])
        self.newParam.set_value(value)