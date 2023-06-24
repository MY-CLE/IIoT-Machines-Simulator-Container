class EmptySetException(Exception):
    def __init__(self):
        super().__init__("Result set is empty.")