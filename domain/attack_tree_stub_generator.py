from domain.tara import Tara
from utilities.error_logger import IErrorLogger

class AttackTreeStubGenerator:
    """
    A class to generate starting files for attack trees for all threats,
    i.e. combinations of assets and security properties.
    """

    def __init__(self, error_logger: IErrorLogger):
        """
        Initializes the AttackTreeStubGenerator with an error logger.
        
        :param error_logger: An instance of IErrorLogger to log errors.
        """
        self.error_logger = error_logger

    def generate_stubs(self, tara: Tara) -> None:
        pass