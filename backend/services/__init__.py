# Services package

class ModelNotReadyError(Exception):
    """Raised when an inference endpoint is called before models are trained."""
    pass

