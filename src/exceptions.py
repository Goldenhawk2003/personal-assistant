class DeviceNotFoundError(Exception):
    """Raised when a device is not found."""
    pass

class DeviceConnectionError(Exception):
    """Raised when there is a connection error with a device."""
    pass

class UnkownCommandError(Exception):
    """Raised when an unknown command is received."""
    pass