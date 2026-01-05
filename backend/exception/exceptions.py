

class ShipmentError(Exception):
    """Base class for all shipment-related errors"""
    pass

class ShipmentValidationError(ShipmentError):
    """Raised when the form data is empty or invalid"""
    pass

class DuplicateShipmentError(ShipmentError):
    """Raised if a shipment reference already exists"""
    pass
