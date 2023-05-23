from opcua import Client
import logging
import socket
import time
import random

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')
logging.getLogger("opcua").setLevel(logging.WARNING)

def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class OPCUAClient:

    def __init__(self):
        self.client = Client(f"opc.tcp://{getIPAddress()}:4840")
        self.client.connect()
        self.data_variables = ["Runtime", "Coolant_Level", "Power_Consumption", "Power_Laser", "Idle_Time"]
        self.nameIndex = self.client.get_namespace_index("MOUSP") # namespace Machinesimulator OPC-UA Server Parameter - Index = 2
        self.node = self.client.get_root_node()

    def getParam(self):
        for i in range(len(self.data_variables)):
            self.param = self.node.get_child(["0:Objects", f"{self.nameIndex}:Parameters", f"{self.nameIndex}:{self.data_variables[i]}"])
            logging.info(self.param.get_browse_name().Name + ": " + str(self.param.get_value()))

    def changeParam(self, param, value):
        print(str(self.node) + " " + str(self.node.get_browse_name().Name))
        self.newParam = self.client.get_node(f"ns={self.nameIndex};s={param}").set_value(value)
        self.names = self.client.get


if __name__ == "__main__":
    ouaClient = OPCUAClient()
    logging.info("Client started")
    try:
        while True:
            ouaClient.changeParam("Runtime", random.randint(0, 100))
            ouaClient.getParam()
            time.sleep(5)
    finally:
        ouaClient.client.disconnect()
        logging.info("Client stopped")