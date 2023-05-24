
class DatabaseObject(object):

    def __init__(self, resultRow: tuple) -> None:
        self.resultRow: tuple = resultRow

    def getResultRow(self) -> tuple:
        return self.resultRow
    
    def __str__(self) -> str:
        return str(self.resultRow)
