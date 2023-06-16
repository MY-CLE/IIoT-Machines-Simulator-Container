from database.orm.databaseObject import DatabaseObject

class Protocol(object):

    def __init__(self, protocolID: int, protocolDescription: str) -> None:
        self.protocolID: int = protocolID
        self.protocolDescription: str = protocolDescription

    def getProtocolID(self) -> int:
        return self.protocolID

    def getProtocolDescription(self) -> str:
        return self.protocolDescription