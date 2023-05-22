from opcua import Server
import logging
import time

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')

class OPCUAServer:
    
        def __init__(self):
            self.server = Server()
            self.server.set_endpoint("opc.tcp://127.0.0.1:4840")
            #self.server.set_server_name("OPCUA Server")
            self.server.register_namespace("OPCUA Server")
            self.objects = self.server.get_objects_node()
            self.param = self.objects.add_object(self.server.get_namespace_index("OPCUA Server"), "Parameters")

        def addParam(self, name, value):
            self.param.add_variable(self.server.get_namespace_index("OPCUA Server"), name, value).set_writable()
            

if __name__ == "__main__":
    ouaServer = OPCUAServer()
    ouaServer.addParam("Runtime", 0)
    ouaServer.server.start()
    logging.info("Server started")
    try:
        while True:
            time.sleep(5)
    finally:
        ouaServer.server.stop()
        logging.info("Server stopped")