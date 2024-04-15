class EmptyInputException(Exception):
    def __init__(self, message="You haven't selected an input method"):
        super().__init__(message)
