from opcua import Client
import logging
import time

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO, encoding='utf-8')


class OPCUAClient:

    def __init__(self):
        self.client = Client("opc.tcp://127.0.0.1:4840")
        self.client.connect()

    def getParam(self):
        self.param = self.client.get_objects_node().get_children()[0].get_children()[0]


if __name__ == "__main__":
    ouaClient = OPCUAClient()
    ouaClient.getParam()
    logging.info("Client started")
    try:
        while True:
            time.sleep(5)
    finally:
        ouaClient.client.disconnect()
        logging.info("Client stopped")