from database.orm.databaseObject import DatabaseObject
from database.orm.notification.notifcation import Notification

class Error(Notification):
    
    def __init__(self, databaseObject: DatabaseObject) -> None:
        super().__init__(databaseObject)

    def __str__(self) -> str:
        return f"errorID: {self.ID}, errorType: {self.type}"