class PyCricinfoException(Exception):
    """
    Generic exception
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class PageNotFoundException(PyCricinfoException):
    """
    Exception used when an attempt has been made to access a non existent page
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
