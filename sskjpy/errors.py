# coding=utf-8


class SSKJException(Exception):
    """
    Base exception class for every other exception.
    """
    pass


class NotFound(SSKJException):
    """
    Raised when the word can't be found.
    """
    pass
