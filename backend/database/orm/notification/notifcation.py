from database.orm.databaseObject import DatabaseObject

class Notification(object):

    def __init__(self, databaseObject: DatabaseObject) -> None:
        self.ID: int = databaseObject.getResultRow()[0]
        self.type: str = databaseObject.getResultRow()[1]

    def getID(self) -> int:
        return self.ID
    
    def getType(self) -> str:
        return self.type

    def __str__(self) -> str:
        return f"ID: {self.ID}, type: {self.type}"