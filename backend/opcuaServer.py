from opcua import Server
import logging
import socket
import time

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')

def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

class OPCUAServer:
    
        def __init__(self):
            self.server = Server()
            self.server.set_endpoint(f"opc.tcp://{getIPAddress()}:4840")
            self.server.set_server_name("Machinesimulator OPC-UA Server")
            self.regName = self.server.register_namespace("MOUSP") # namespace Machinesimulator OPC-UA Server Parameter

            self.param = self.server.get_objects_node().add_object(self.regName, "Parameters")

        def setParameter(self):
            self.param.add_variable(self.regName, "Runtime", 0).set_writable()
            self.param.add_variable(self.regName, "Coolant_Level", 0).set_writable()
            self.param.add_variable(self.regName, "Power_Consumption", 0).set_writable()
            self.param.add_variable(self.regName, "Power_Laser", 0).set_writable()
            self.param.add_variable(self.regName, "Idle_Time", 0).set_writable()
            

if __name__ == "__main__":
    ouaServer = OPCUAServer()
    ouaServer.setParameter()
    ouaServer.server.start()
    logging.info("Server started")
    try:
        while True:
            time.sleep(5)
    finally:
        ouaServer.server.stop()
        logging.info("Server stopped")