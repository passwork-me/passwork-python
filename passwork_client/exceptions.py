class PassworkError(ValueError):
    """
    Base exception for Passwork client errors.
    Allows specifying an error code along with the message.
    """
    def __init__(self, message, code = None):
        super().__init__(message)
        self.code = code 
