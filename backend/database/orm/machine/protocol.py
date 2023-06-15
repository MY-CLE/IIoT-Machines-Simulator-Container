from database.orm.databaseObject import DatabaseObject

class Protocol(object):

    def __init__(self, databaseObject: DatabaseObject):
        self.protocolID: int = databaseObject.getResultRow()[0]
        self.protocolDescription: str = databaseObject.getResultRow()[1]

    def getProtocolID(self) -> int:
        return self.protocolID

    def getProtocolDescription(self) -> str:
        return self.protocolDescription