class DataBaseException(Exception):
    """This exception is raised when there is a problem with connection or reading from the database"""


class OverInstancesException(Exception):
    """This exception is raised during to attempt to create more instances of the class than it was expected.
    Usually it applies to singleton classes"""
