from opcua import Server

import socket
import logging

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')

# Get the IP Address of the machine
def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

# OPC-UA Server
# Server sets the object and variable for the client to read and write
class OPCUAServer:
    
    def __init__(self) -> None:
        self.server = Server()
        self.server.set_endpoint(f"opc.tcp://{getIPAddress()}:4840")
        self.server.set_server_name("Machinesimulator OPC-UA Server")
        self.regName = self.server.register_namespace("MOUSP") # namespace Machinesimulator OPC-UA Server Parameter

        self.param = self.server.get_objects_node().add_object(self.regName, "Parameters")

        self.setParameter()

    # Start the server and log the status
    def startServer(self) -> None:
        try:
            self.server.start()
            logging.info("OPCUA Server started")
        except:
            logging.error("OPCUA Server is shutting down")
            self.server.stop()
            logging.error("OPCUA Server is stopped")

    # Set the variables for the client to read and write the parameters
    def setParameter(self) -> None:
        self.param.add_variable(self.regName, "Runtime", 0).set_writable()
        self.param.add_variable(self.regName, "Idle_Time", 0).set_writable()
        self.param.add_variable(self.regName, "Coolant_Level", 0).set_writable()
        self.param.add_variable(self.regName, "Power_Consumption", 0).set_writable()
        self.param.add_variable(self.regName, "Capacity_Laser_Module", 0).set_writable()
        self.param.add_variable(self.regName, "Total_Items", 0).set_writable()
        self.param.add_variable(self.regName, "Program_Runtime", 0).set_writable()
        self.param.add_variable(self.regName, "Target_Amount", 0).set_writable()
        self.param.add_variable(self.regName, "Current_Amount", 0).set_writable()
        self.param.add_variable(self.regName, "Coolant_Consumption", 0).set_writable()
        self.param.add_variable(self.regName, "Laser_Module_Weardown", 0).set_writable()
        self.param.add_variable(self.regName, "Laser_Power_Consumption", 0).set_writable()
        self.param.add_variable(self.regName, "Time_Per_Item", 0).set_writable()
