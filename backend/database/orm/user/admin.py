from database.orm.databaseObject import DatabaseObject

class Admin(object):

    def __init__(self, databaseObject: DatabaseObject) -> None:
        self.ID: int = databaseObject.getResultRow()[0]
        self.password: str = databaseObject.getResultRow()[1]

    def getID(self) -> int:
        return self.ID
    
    def getPassword(self) -> str:
        return self.password
    
    def __str__(self) -> str:
        return f"adminID: {self.ID}, adminPassword: {self.password}"