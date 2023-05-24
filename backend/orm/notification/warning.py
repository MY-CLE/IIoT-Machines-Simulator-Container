from orm.databaseObject import DatabaseObject
from orm.notification.notifcation import Notification

class Warning(Notification):

    def __init__(self, databaseObject: DatabaseObject) -> None:
        super().__init__(databaseObject)
    
    def __str__(self) -> str:
        return f"warningID: {self.ID}, warningType: {self.type}"